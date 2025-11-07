
import pygame
import time
import os
pygame.init()
timeBegin= pygame.time.get_ticks()
game_over=False
def timer(timeBegin,game_over):
    PATH = "./speedruntime.txt"
    if game_over:
        timeEnd = pygame.time.get_ticks()
        print(timeBegin)
        print(timeEnd)
        speedrun_time = timeEnd - timeBegin
        if os.path.isfile(PATH) and os.access(PATH, os.R_OK):
            print("File exists and is readable")
            with open(PATH, "r") as f:
                lines=f.readlines()
                print(lines)
                lines[0]=str(speedrun_time)
            with open(PATH, "w") as f:
                f.writelines(lines)
            with open(PATH, "r") as f:    
                print(f.readlines())
            return speedrun_time
        else:
            print("Either the file is missing or not readable")
timer(timeBegin,game_over)
time.sleep(12.5)
game_over=True
print(f"{timer(timeBegin,game_over)/1000:.2f}s")
PATH = "./speedruntime.txt"
if game_over:
    timeEnd = pygame.time.get_ticks()
    print(timeBegin)
    print(timeEnd)
    speedrun_time = timeEnd - timeBegin
    if os.path.isfile(PATH) and os.access(PATH, os.R_OK):
        print("File exists and is readable")
        with open(PATH, "r") as f:
            lines=f.readlines()
            print(lines)
            lines[0]=str(speedrun_time)
        with open(PATH, "w") as f:
                f.writelines(lines)
        with open(PATH, "r") as f:    
                print(f.readlines())
    else:
            print("Either the file is missing or not readable")
