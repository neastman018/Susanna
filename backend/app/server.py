from contextlib import asynccontextmanager
import datetime
import os
from fastapi import Depends, FastAPI
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from colorama import Fore, Style, init
from typing import Dict, Any, Union
from app.models.data_models import AlarmModel
import asyncio




on_Pi = True
try:
    import RPi.GPIO as GPIO
except ImportError:
    on_Pi = False
    GPIO = None
    print("Buttons not in use")
    
# --- 1. Decide which driver to import ---
if on_Pi:
    # Attempt to import the real hardware driver
    from hal.button_driver import ButtonDriver as ActualButtonDriver
    print("Running in RPi Environment: Loading real GPIO drivers.")
else:
    # Fallback to the mock driver
    from app.utils.mock_button_driver import MockButtonDriver as ActualButtonDriver
    print("Running in Development Environment: Loading mock GPIO drivers.")
    
# --- Service and Model Imports ---
from app.models.data_models import QuoteModel 
from app.services.data_service import DataService 
from app.services.application_state_service import ASService
from app.services.alarm_service import AlarmService
from app.services.gpio_service import GpioService, ButtonDriverInterface # Need ButtonDriverInterface for typing

    
alarm1 = AlarmModel(
    alarm_time="11:39",
    start_date="2025-12-16",
    repeat="Weekly",
    day_of_week=["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],
    sound="Thats_Life.mp3",
    label="Weekday Wake Up",
    armed=False
)

alarm2 = AlarmModel(
    alarm_time="16:24",
    start_date="2025-12-16",
    repeat="Weekly",
    day_of_week=["Saturday", "Sunday"],
    sound="Thats_Life.mp3",
    label="Weekend Wake Up",
    armed=False
)

buttons: Dict[str, int] ={
    'PrimaryButton': 6,
    'SecondaryButton': 5,
    'EncoderButton': 4,
}

# Global variables for service instances and the background task
data_manager: DataService
app_state: ASService
alarm_manager: AlarmService
gpio_manager: GpioService
alarm_task: asyncio.Task  # Store the reference to the background task


def get_data_service() -> DataService:
    """Dependency function to inject the initialized DataService."""
    if data_manager is None:
        raise Exception(status_code=503, detail="DataService not initialized")
    return data_manager 


def get_alarm_service() -> AlarmService:
    """Dependency function to inject the initialized AlarmService."""
    if alarm_manager is None:
        raise Exception(status_code=503, detail="AlarmService not initialized")
    return alarm_manager 

def get_state_service() -> AlarmService:
    """Dependency function to inject the initialized AlarmService."""
    if app_state is None:
        raise Exception(status_code=503, detail="AlarmService not initialized")
    return app_state 

# --- Background Worker Function ---
async def alarm_checker_worker(alarm_manager: AlarmService, app_state: ASService):
    """
    The continuous task that periodically calls the alarm checking logic.
    """
    CHECK_INTERVAL_SECONDS = 15  # Check the time every 15 seconds
    
    print(f"{Fore.YELLOW}Background Alarm Checker starting... Interval: {CHECK_INTERVAL_SECONDS}s{Style.RESET_ALL}")
    
    while True:
        try:
            # Call the synchronous alarm checking method
            alarm_manager.activate_next_alarm(current_time=datetime.datetime.now())
            
            # Wait for the next interval
            await asyncio.sleep(CHECK_INTERVAL_SECONDS)
        
        except asyncio.CancelledError:
            # Clean shutdown when the lifespan exits
            print(f"{Fore.RED}Background Alarm Checker cancelled.{Style.RESET_ALL}")
            break
        except Exception as e:
            # Log any unexpected errors and continue the loop
            print(f"{Fore.RED}Alarm Checker encountered an error: {e}{Style.RESET_ALL}")
            await asyncio.sleep(CHECK_INTERVAL_SECONDS)


@asynccontextmanager
async def lifespan(app: FastAPI):
    global data_manager, app_state, alarm_manager, gpio_manager, alarm_task

    # --- 2. Initialize Dependencies ---
    data_manager = DataService()
    app_state = ASService()
    alarm_manager = AlarmService(data_service=data_manager, as_service=app_state)
    

    # Clear and insert alarms for testing purposes
    data_manager.clear_alarms()
    data_manager.insert_alarm(alarm1)
    data_manager.insert_alarm(alarm2)
    
    next_alarm = alarm_manager.find_next_alarm(datetime.date.today(), datetime.datetime.now().time())
    app_state.set_alarm_time(next_alarm.alarm_time if next_alarm else "N/A")
    app_state.set_alarm_armed(next_alarm.armed if next_alarm else False)
    
    # --- 3. Initialize ALL Button Drivers ---
    button_drivers: Dict[str, ButtonDriverInterface] = {}
    for name, pin in buttons.items():
        # Instantiate the correct driver (Real or Mock) for each physical pin
        driver_instance = ActualButtonDriver(pin=pin)
        button_drivers[name] = driver_instance
        print(f"Driver initialized: {name} on pin {pin} using {ActualButtonDriver.__name__}")


    # --- 4. Initialize GPIO Service with the FULL Driver Map ---
    gpio_manager = GpioService(
        app_state=app_state, 
        alarm_handler=alarm_manager, 
        button_drivers=button_drivers # Pass the dictionary map
    )
    
    # --- 5. Start Background Task ---
    gpio_manager.start_polling() 
    alarm_task = asyncio.create_task(alarm_checker_worker(alarm_manager=alarm_manager, app_state=app_state))
    print(f"{Fore.YELLOW}FastAPI Server and Services Started!{Style.RESET_ALL}")
    
    yield
    
    # --- 6. Shutdown ---
    print(f"{Fore.RED}--- FastAPI Shutdown Sequence ---{Style.RESET_ALL}")
    
    # CRITICAL CHANGE: Gracefully cancel the background task
    alarm_task.cancel()
    await asyncio.gather(alarm_task, return_exceptions=True)
    await gpio_manager.shutdown()
    
    
app = FastAPI(lifespan=lifespan)
init(autoreset=True)


origins = [
    "http://localhost:3000",
    "localhost:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)
# ==========================================================================================================
# =================================== API ENDPOINTS ========================================================
# =============================== Called Periodically ======================================================
# ==========================================================================================================\
    
# --- Dependency Injectors (Used by FastAPI Depends) ---



# Sends to quote to the frontend. Will be called periodically based on the hook
@app.get("/api/quotes", tags=["info"])
async def get_quote(service: DataService = Depends(get_data_service)) -> QuoteModel:
    
    quote_data = service.get_random_quote()
    print(quote_data)
    return quote_data

@app.get("/api/alarm", tags=["info"]) #API Endpoint is alarm
async def get_alarm(service: AlarmService = Depends(get_state_service)) -> dict:
    
    
    next_alarm_time = service.get_alarm_time()
    armed = service.get_alarm_armed()       
    
    return {
        "alarm_time": next_alarm_time,
        "armed": armed
    }   
# ==========================================================================================================