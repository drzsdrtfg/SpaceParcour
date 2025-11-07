import pygame
import os
import sys
import time as t
pygame.init()
time = pygame.time.Clock()
pygame.mixer.init()
if not pygame.mixer.get_init():
    print("DEBUGGING: Sound player not initialized")
menuClick1 = pygame.mixer.Sound("audio/Clicks/Click.wav")
menuClick2 = pygame.mixer.Sound("audio/Clicks/Click_1.wav")
menuClick3 = pygame.mixer.Sound("audio/Clicks/Click_2.wav")
channel = pygame.mixer.find_channel()
choice_Order = []
max_shield = 100
current_shield = 100
max_energy = 100
current_energy = 0
playerX, playerY= 100,100
gtime=0
cooldownJump=1800
lastJump=0
playerYaccel=0.03
playerYspeed=0
on_ground=False
jumped=0
shield_BLUE=0, 177, 229
font = pygame.font.Font("font/CrossflyDisplay.otf", 35)
speedrun_start_time = None
speedrun_time = 0
speedrun_saved = False
game_over = False
def menuClicksAudio():
    if len(choice_Order) == 3:
        channel.queue(menuClick1)
        choice_Order.clear()
    elif len(choice_Order) == 2:
        channel.queue(menuClick3)
        choice_Order.append("menuClick3")
    elif len(choice_Order) == 1:
        channel.queue(menuClick2)
        choice_Order.append("menuClick2")
    else: 
        channel.queue(menuClick1)
        choice_Order.append("menuClick1")
def scale_button(button_img, button_rect, hovered):
    if hovered:
        scale_factor = 1.1
        new_size = (int(button_rect.width * scale_factor), int(button_rect.height * scale_factor))
        scaled_img = pygame.transform.scale(button_img, new_size)
        scaled_rect = scaled_img.get_rect(center=button_rect.center)
        return scaled_img, scaled_rect
    else:
        return button_img, button_rect
def draw_rounded_shield_bar(x, y, width, height, shield, max_shield, radius=10):
    pygame.draw.rect(window, "white", (x, y, width, height), border_radius=radius)
    shield_ratio = shield / max_shield
    pygame.draw.rect(window, shield_BLUE, (x, y, width * shield_ratio, height), border_radius=radius)
    pygame.draw.rect(window, "black", (x, y, width, height), 5, border_radius=radius)
def draw_rounded_energy_bar(x, y, width, height, energy, max_energy, radius=10):
    pygame.draw.rect(window, "white", (x, y, width, height), border_radius=radius)
    energy_ratio = energy / max_energy
    pygame.draw.rect(window, "yellow", (x, y, width * energy_ratio, height), border_radius=radius)
    pygame.draw.rect(window, "black", (x, y, width, height), 5, border_radius=radius)
width = 1920
height = 1080
relative_Button_position = 200
play_Button_position = 300
game_mode="menu"
window = pygame.display.set_mode((width, height))
pygame.display.set_caption("Space runner")
pygame.mouse.set_visible(False)
background = pygame.image.load("graphics/sun2dnew.png").convert()
play_Button = pygame.image.load("graphics/playButton.png").convert_alpha()
settings_Button = pygame.image.load("graphics/settingsButton.png").convert_alpha()
quit_Button = pygame.image.load("graphics/quitButton.png").convert_alpha()
back_Button = pygame.image.load("graphics/backButton.png").convert_alpha()
cursor = pygame.image.load("graphics/cursor2d.png").convert_alpha()
levels_image = pygame.image.load("graphics/LevelsReal.png").convert_alpha()
levels1_image = pygame.image.load("graphics/Level1Real.png").convert_alpha()
levels2_image = pygame.image.load("graphics/Level2Real.png").convert_alpha()
levels3_image = pygame.image.load("graphics/Level3Real.png").convert_alpha()
levels4_image = pygame.image.load("graphics/Level4Real.png").convert_alpha()
levels5_image = pygame.image.load("graphics/Level5Real.png").convert_alpha()
playerCharacter = pygame.image.load("graphics/realAstro2d.png").convert_alpha()
platform1 = pygame.image.load("graphics/platformReal1.png").convert_alpha()
playerCharacterLeft=pygame.transform.flip(playerCharacter, flip_y=False, flip_x=True)
currentPlayerCharacter=playerCharacter
playAudio = False
lastOnButton = False
NowOnButton = False
def menu(playAudio, lastOnButton, NowOnButton, game_mode):
    cursor_pos = pygame.mouse.get_pos()
    quit_Button_rect = quit_Button.get_rect()
    quit_Button_rect.center = (width / 2, 2 * relative_Button_position + play_Button_position)
    settings_Button_rect = settings_Button.get_rect()
    settings_Button_rect.center = (width / 2, relative_Button_position + play_Button_position)
    play_Button_rect = play_Button.get_rect()
    play_Button_rect.center = (width / 2, play_Button_position)
    cursor_rect = cursor.get_rect()
    cursor_rect.center = (cursor_pos)
    play_hovered = play_Button_rect.contains(cursor_rect)
    settings_hovered = settings_Button_rect.contains(cursor_rect)
    quit_hovered = quit_Button_rect.contains(cursor_rect)
    play_img, play_rect = scale_button(play_Button, play_Button_rect, play_hovered)
    settings_img, settings_rect = scale_button(settings_Button, settings_Button_rect, settings_hovered)
    quit_img, quit_rect = scale_button(quit_Button, quit_Button_rect, quit_hovered)
    if quit_hovered:
        NowOnButton = True
        if pygame.mouse.get_pressed()[0]:
            pygame.quit()
            sys.exit()
        elif not lastOnButton:
            lastOnButton = True
            playAudio = True
            menuClicksAudio()
    elif settings_hovered:
        NowOnButton = True
        if pygame.mouse.get_pressed()[0]:
            pygame.quit()
            sys.exit()
        elif not lastOnButton:
            lastOnButton = True
            playAudio = True
            menuClicksAudio()
    elif play_hovered:
        NowOnButton = True
        if pygame.mouse.get_pressed()[0]:
            game_mode = "Levels"
        elif not lastOnButton:
            lastOnButton = True
            playAudio = True
            menuClicksAudio()
    else:
        lastOnButton = False
        playAudio = False
        NowOnButton = False
    window.blit(background, (0, 0))
    window.blit(play_img, play_rect)
    window.blit(settings_img, settings_rect)
    window.blit(quit_img, quit_rect)
    window.blit(cursor, cursor_pos)
    return playAudio, lastOnButton, NowOnButton, game_mode
def lvlScreen(playAudio, lastOnButton, NowOnButton, game_mode):
    cursor_pos = pygame.mouse.get_pos()
    cursor_rect = cursor.get_rect()
    cursor_rect.center = (cursor_pos)
    levels_image_rect = levels_image.get_rect()
    levels_image_rect.center = (width / 2, 220)
    levels1_image_rect = levels1_image.get_rect()
    levels1_image_rect.center = (480, height/2)
    levels2_image_rect = levels2_image.get_rect()
    levels2_image_rect.center = (730, height/2)
    levels3_image_rect = levels3_image.get_rect()
    levels3_image_rect.center = (980, height/2)
    levels4_image_rect = levels4_image.get_rect()
    levels4_image_rect.center = (1230, height/2)
    levels5_image_rect = levels5_image.get_rect()
    levels5_image_rect.center = (1480, height/2)
    back_Button_rect = back_Button.get_rect()
    back_Button_rect.center = (340, 900)
    levels1_image_hovered = levels1_image_rect.contains(cursor_rect)
    levels2_image_hovered = levels2_image_rect.contains(cursor_rect)
    levels3_image_hovered = levels3_image_rect.contains(cursor_rect)
    levels4_image_hovered = levels4_image_rect.contains(cursor_rect)
    levels5_image_hovered = levels5_image_rect.contains(cursor_rect)
    back_Button_hovered =   back_Button_rect.contains(cursor_rect)
    levels1_image_img, levels1_rect = scale_button(levels1_image, levels1_image_rect, levels1_image_hovered)
    levels2_image_img, levels2_rect = scale_button(levels2_image, levels2_image_rect, levels2_image_hovered)
    levels3_image_img, levels3_rect = scale_button(levels3_image, levels3_image_rect, levels3_image_hovered)
    levels4_image_img, levels4_rect = scale_button(levels4_image, levels4_image_rect, levels4_image_hovered)
    levels5_image_img, levels5_rect = scale_button(levels5_image, levels5_image_rect, levels5_image_hovered)
    back_Button_img, back_rect = scale_button(back_Button, back_Button_rect, back_Button_hovered)
    if levels1_image_hovered:
        NowOnButton = True
        if pygame.mouse.get_pressed()[0]:
            game_mode = "lvl1"
        elif not lastOnButton:
            lastOnButton = True
            playAudio = True
            menuClicksAudio()
    elif levels2_image_hovered:
        NowOnButton = True
        if pygame.mouse.get_pressed()[0]:
            pygame.quit()
            sys.exit()
        elif not lastOnButton:
            lastOnButton = True
            playAudio = True
            menuClicksAudio()
    elif levels3_image_hovered:
        NowOnButton = True
        if pygame.mouse.get_pressed()[0]:
            pygame.quit()
            sys.exit()
        elif not lastOnButton:
            lastOnButton = True
            playAudio = True
            menuClicksAudio()
    elif levels4_image_hovered:
        NowOnButton = True
        if pygame.mouse.get_pressed()[0]:
            pygame.quit()
            sys.exit()
        elif not lastOnButton:
            lastOnButton = True
            playAudio = True
            menuClicksAudio()
    elif levels5_image_hovered:
        NowOnButton = True
        if pygame.mouse.get_pressed()[0]:
            pygame.quit()
            sys.exit()
        elif not lastOnButton:
            lastOnButton = True
            playAudio = True
            menuClicksAudio()
    elif back_Button_hovered:
        NowOnButton = True
        if pygame.mouse.get_pressed()[0]:
            game_mode = "menu"
        elif not lastOnButton:
            lastOnButton = True
            playAudio = True
            menuClicksAudio()
    else:
        lastOnButton = False
        playAudio = False
        NowOnButton = False
    window.blit(background, (0, 0))
    window.blit(levels_image, levels_image_rect)
    window.blit(levels1_image_img, levels1_rect)
    window.blit(levels2_image_img, levels2_rect)
    window.blit(levels3_image_img, levels3_rect)
    window.blit(levels4_image_img, levels4_rect)
    window.blit(levels5_image_img, levels5_rect)
    window.blit(back_Button_img, back_rect)
    window.blit(cursor, cursor_pos)
    return playAudio, lastOnButton, NowOnButton, game_mode
def lvl1(playAudio, lastOnButton, NowOnButton, game_mode, current_energy, max_energy, keys, playerX, playerY, playerCharacter, playerCharacterLeft, currentPlayerCharacter, gtime, cooldownJump, lastJump, playerYaccel, playerYspeed, on_ground, jumped):
    global speedrun_time, speedrun_start_time, speedrun_saved, game_over
    if speedrun_start_time is None:
        speedrun_start_time = pygame.time.get_ticks()
    cursor_pos = pygame.mouse.get_pos()
    playerCharacter_rect = playerCharacter.get_rect()
    playerCharacter_rect.midbottom = (playerX, playerY)
    cursor_rect = cursor.get_rect()
    cursor_rect.center = (cursor_pos)
    platform1_rect = platform1.get_rect()
    platform1_rect.center = (250,1000)
    PATH = "./speedruntime.txt"
    if playerCharacter_rect.colliderect(platform1_rect):
        print("Collision!")
        
    if not game_over and keys[pygame.K_p]:
        game_over = True
        speedrun_time = pygame.time.get_ticks() - speedrun_start_time
        print(f"{speedrun_time/1000:.2f}s")
        if os.path.isfile(PATH) and os.access(PATH, os.R_OK):
            with open(PATH, "r") as f:
                lines=f.readlines()
            if len(lines) == 0:
                lines = [str(speedrun_time)]
            else:
                lines[0]=str(speedrun_time)
            with open(PATH, "w") as f:
                f.writelines(lines)
        else:
            print("Either the file is missing or not readable")
    elapsed = speedrun_time if game_over else (pygame.time.get_ticks() - speedrun_start_time)
    timerText = font.render(f"Elapsed time: {elapsed/1000:.2f}", True, shield_BLUE)
    window.blit(background, (0, 0))
    window.blit(cursor, cursor_pos)
    window.blit(platform1, platform1_rect)
    window.blit(timerText, (1100,100))
    playerYspeed+=playerYaccel

    if playerY+playerYspeed<900:
        on_ground= False
    else: 
        on_ground=True

    if on_ground:
        print("No gravitation")
        playerYspeed=0
    else:
        
        playerY+=playerYspeed**2
    if current_energy<max_energy:
        current_energy+=0.1
    if (pygame.time.get_ticks()-lastJump)>cooldownJump:
        if (keys[pygame.K_UP] or keys[pygame.K_w]) and playerY-6>0:
            jumped=0
            lastJump=pygame.time.get_ticks()
    if jumped>-40:
        jumped+=-1
        playerY+=-5    
    if (keys[pygame.K_LEFT] or keys[pygame.K_a]) and playerX-3>0:
        currentPlayerCharacter=playerCharacterLeft
        playerX+=-3
    elif (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and playerX+3<1800:
        playerX+=3
        currentPlayerCharacter=playerCharacter


    elif (keys[pygame.K_DOWN] or  keys[pygame.K_s]) and playerY+3<1000:
        playerY+=3
    if (keys[pygame.K_LEFT] or keys[pygame.K_a]) and (keys[pygame.K_UP] or keys[pygame.K_w]) and playerX-3>0 and playerY-6>0:
        currentPlayerCharacter=playerCharacterLeft
        playerX+=-3
        jumped=0    
    if (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and (keys[pygame.K_UP] or keys[pygame.K_w]) and playerX+3<1800 and playerY-6>0:
        currentPlayerCharacter=playerCharacterLeft
        playerX+=3
        jumped=0    


    draw_rounded_shield_bar(50, 100, 500, 60, current_shield, max_shield)
    draw_rounded_energy_bar(50, 200, 500, 60, current_energy, max_energy)
    window.blit(currentPlayerCharacter, (playerX,playerY))

    return playAudio, lastOnButton, NowOnButton, game_mode, current_energy, playerX, playerY, playerCharacter, playerCharacterLeft, currentPlayerCharacter, gtime, cooldownJump, lastJump, playerYaccel, playerYspeed, on_ground, jumped
while True:
    mouse_pos = pygame.mouse.get_pos()
    keys = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    if game_mode == "menu":
        playAudio, lastOnButton, NowOnButton, game_mode = menu(playAudio, lastOnButton, NowOnButton, game_mode)
    elif game_mode == "Levels":
        playAudio, lastOnButton, NowOnButton, game_mode = lvlScreen(playAudio, lastOnButton, NowOnButton, game_mode)
    elif game_mode == "lvl1":
        playAudio, lastOnButton, NowOnButton, game_mode, current_energy, playerX, playerY, playerCharacter, playerCharacterLeft, currentPlayerCharacter, gtime, cooldownJump, lastJump, playerYaccel, playerYspeed, on_ground, jumped = lvl1(playAudio, lastOnButton, NowOnButton, game_mode, current_energy, max_energy, keys, playerX, playerY, playerCharacter, playerCharacterLeft, currentPlayerCharacter, gtime, cooldownJump, lastJump, playerYaccel, playerYspeed, on_ground, jumped)
    pygame.display.update()
    time.tick(120)
