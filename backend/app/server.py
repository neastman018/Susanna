from fastapi import FastAPI, WebSocket, WebSocketDisconnect, File, UploadFile
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from pydantic import BaseModel
import time
from colorama import Fore, Style, init
from io import BytesIO
from datetime import datetime
import ast
from fastapi.responses import JSONResponse
import json
from app.alarm.alarm import Alarm
from app.quotes.quotes import get_random_quote
import RPi.GPIO as GPIO
import asyncio
from app.button.button import Button, wait_for_button_state_change, button_poll_task

PIN1= 6
PIN2 = 5
ROTARY_PIN = 4

NUM_PIXELS = 60
DEFAULT_COLOR = (255, 255, 255)

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

test_alarm = Alarm()
button1: Button = None       # <--- Declared, but NOT initialized here
poll_task: asyncio.Task = None




origins = [
    "http://localhost:3000",
    "localhost:3000"
]

class QuoteModel(BaseModel):
    quote: str
    author: str
    
class AlarmModel(BaseModel):
    alarm_time: str
    armed: bool # Remember an unauthorized armed alarm is a terror attack to sleeping roommates
    
# ==========================================================================================================
# =================================== FastAPI Startup ======================================================
# ==========================================================================================================
    
    
@asynccontextmanager
async def lifespan(app: FastAPI):
    global button1, poll_task
    
    with open('config.json', 'r') as config_file:
        config = json.load(config_file)
        alarm_sound = config.get('ALARM', {}).get('ALARM_SOUND', [])
        print(f"Wake up time for today: {alarm_sound}")
        
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    
    button1 = Button(pin=PIN1)
    button1.init_button()
    # Startup code can go here
    test_alarm.init("Peaky_Blinders.mp3")

    poll_task = asyncio.create_task(button_poll_task(button1))
    print(f"{Fore.YELLOW}FastAPI Server and Button Polling Task Started!{Style.RESET_ALL}")
    
    yield
    # 🧹 SHUTDOWN: Cleanup Resources
    print("Executing shutdown routine...")
    if poll_task:
        poll_task.cancel()
    GPIO.cleanup()
    
app = FastAPI(lifespan=lifespan)
init(autoreset=True)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# Do not need unless I need data from the frontend
# class ConnectionManager:
#     def __init__(self):
#         self.active_connections: list[WebSocket] = []
    
#     async def connect(self, websocket: WebSocket):
#         await websocket.accept()
#         self.active_connections.append(websocket)

#     def disconnect(self, websocket: WebSocket):
#         self.active_connections.remove(websocket)

#     async def send_personal_message(self, message: str, websocket: WebSocket):
#         await websocket.send_text(message)
    
#     #broadcasts to everyone awaiting messages
#     async def broadcast(self, message: str):
#         for connection in self.active_connections:
#             await connection.send_text(message)

    
# manager = ConnectionManager()
# ==========================================================================================================
# =================================== Backend Events =======================================================
# ==========================================================================================================


@app.on_event("startup")
async def startup_event():
    """
    Initializes GPIO and starts the button polling task when the server starts.
    """
    global button1
    
    # Use BCM numbering mode
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    
    # Initialize the button on BCM pin 14 (example pin)
    button1 = Button(pin=14) 
    button1.init_button()
    
    # Start the continuous polling task as a background task.
    # This runs the button's synchronous polling logic without blocking the server.
    asyncio.create_task(button_poll_task(button1))
    print(f"{Fore.YELLOW}FastAPI Server and Button Polling Task Started!{Style.RESET_ALL}")

@app.on_event("shutdown")
def shutdown_event():
    """
    Cleans up GPIO when the server shuts down.
    """
    print(f"{Fore.YELLOW}FastAPI Server shutting down. Cleaning up GPIO.{Style.RESET_ALL}")
    GPIO.cleanup()


# ==========================================================================================================
# =================================== API ENDPOINTS =========================================================
# ==========================================================================================================

# Sends to quote to the frontend. Will be called periodically based on the hook
@app.get("/api/quotes", tags=["info"])
async def get_quote() -> dict:
    quote_data = get_random_quote()
    return {  
        "quote": quote_data["quote"],
        "author": quote_data["author"]
    }

@app.get("/api/alarm", tags=["info"]) #API Endpoint is alarm
async def get_alarm() -> dict:
    # alarm_time = test_alarm.get_wake_up_time()
    armed = True
    
    return {
        "alarm_time": "6:30 AM",
        "armed": True
    }   
