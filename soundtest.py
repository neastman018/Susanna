from datetime import datetime
from playsound import playsound
import os


if __name__ == '__main__':
    now = datetime.now()
    print(now.hour)
    playsound('alarm/music/Good_MorningV2.mp3')