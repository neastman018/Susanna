import time
import pygame
import multiprocessing


pygame.mixer.init()
alarm = pygame.mixer.music
alarm.load('alarm/music/Good_MorningV2.mp3')


alarm.play()
i = 1

while alarm.get_busy() == True:
    i = i + 1
    print(i)
    time.sleep(3)

#alarm = multiprocessing.Process(target=playsound, args=("alarm/music/" + alarm_sound,))
