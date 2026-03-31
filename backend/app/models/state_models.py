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
import asyncio
from app.button.button import Button, wait_for_button_state_change, button_poll_task, fake_button_poll_task

on_Pi = True
try:
    import RPi.GPIO as GPIO
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
except ImportError:
    on_Pi = False
    GPIO = None
    print("RPi.GPIO not found. Running in non-Raspberry Pi mode.")

PIN1= 6
PIN2 = 5
ROTARY_PIN = 4

NUM_PIXELS = 60
DEFAULT_COLOR = (255, 255, 255)



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
    
    with open('../config.json', 'r') as config_file:
        config = json.load(config_file)
        alarm_sound = config.get('ALARM', {}).get('ALARM_SOUND', [])
        print(f"Wake up time for today: {alarm_sound}")
        
    if on_Pi:
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
        
        
        
    else:
        poll_task = asyncio.create_task(fake_button_poll_task())
        print(f"{Fore.YELLOW}FastAPI Server Started in non-Raspberry Pi mode!{Style.RESET_ALL}")
        
        yield
        # 🧹 SHUTDOWN: Cleanup Resources
        print("Executing shutdown routine...")
        if poll_task:
            poll_task.cancel()
            
            
    
app = FastAPI(lifespan=lifespan)
init(autoreset=True)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)