
import time
from datetime import datetime
from subprocess import run
import os
import json
from alarm.alarm import Alarm


print("Running Test File")

with open('config.json', 'r') as config_file:
            config = json.load(config_file)
            alarm_sound = config.get('ALARM', {}).get('ALARM_SOUND', [])
            print(f"Wake up time for today: {alarm_sound}")
print(f"Wake up time for today: {alarm_sound}")
