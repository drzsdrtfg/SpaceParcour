import pygame
import os
import sys
import json

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
camX, camY=0,0
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
def lvl1(playAudio, lastOnButton, NowOnButton, game_mode, current_energy, max_energy, keys, playerX, playerY, playerCharacter, playerCharacterLeft, currentPlayerCharacter, gtime, cooldownJump, lastJump, playerYaccel, playerYspeed, on_ground, jumped, camX, camY):
   LEVEL_PATH = "SpaceRunner/Level_0.ldtkl"
   with open(LEVEL_PATH, "r", encoding="utf-8") as file:
        level_data = json.load(file)
    #print("You have", len(level_data.get("layerInstances")), "layers in your level")
    #print("You have", level_data.keys(), "layers in your level")
   layers=level_data["layerInstances"]
   for layer in layers:
        print (layer["__identifier"])
        if layer["__identifier"]=="Ground":
            grid_size=layer["__gridSize"]
            tile_img=layer["__tilesetRelPath"]
            tile_img=pygame.image.load(tile_img).convert_alpha()
            tiles=layer["gridTiles"]
            tile_w, tile_h = tile_img.get_size()
        elif layer["__identifier"]=="IntGrid":
            grid_size_Int = layer["__gridSize"]
            width = layer["__cWid"]
            height = layer["__cHei"]
            intgrid = layer["intGridCsv"]
            for i, cell_value in enumerate(intgrid):
                if cell_value == 1:
                x = (i % width) * grid_size_Int
                y = (i // width) * grid_size_Int
   print(len(tiles))
   window.fill((0,0,0))
   for tile in tiles:
        print(tile.get("px"))
        src_rect=pygame.Rect(tile.get("src")[0],tile.get("src")[1], grid_size, grid_size)
        src_rect.clamp_ip(pygame.Rect(0, 0, tile_w, tile_h))
        current_tile = tile_img.subsurface(src_rect).copy()
        if tile.get("f")==0:
            current_tile=pygame.transform.flip(current_tile, False, False)
        elif tile.get("f")==1:
            current_tile=pygame.transform.flip(current_tile, True, False)
        elif tile.get("f")==2:
            current_tile=pygame.transform.flip(current_tile, False, True)
        elif tile.get("f")==3:
            current_tile=pygame.transform.flip(current_tile, True, True)

        window.blit(current_tile,(tile.get("px")[0]-camX,tile.get("px")[1]-camY))
 
   if (keys[pygame.K_LEFT] or keys[pygame.K_a]):
        camX+=-30
   elif (keys[pygame.K_RIGHT] or keys[pygame.K_d]):
        camX+=30
        currentPlayerCharacter=playerCharacter
   elif (keys[pygame.K_DOWN] or  keys[pygame.K_s]):
        camY+=30
   elif (keys[pygame.K_DOWN] or  keys[pygame.K_s]):
        camY-=30
    
   pygame.display.flip() 
   return playAudio, lastOnButton, NowOnButton, game_mode, current_energy, playerX, playerY, playerCharacter, playerCharacterLeft, currentPlayerCharacter, gtime, cooldownJump, lastJump, playerYaccel, playerYspeed, on_ground, jumped, camX, camY
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
        playAudio, lastOnButton, NowOnButton, game_mode, current_energy, playerX, playerY, playerCharacter, playerCharacterLeft, currentPlayerCharacter, gtime, cooldownJump, lastJump, playerYaccel, playerYspeed, on_ground, jumped, camX, camY = lvl1(playAudio, lastOnButton, NowOnButton, game_mode, current_energy, max_energy, keys, playerX, playerY, playerCharacter, playerCharacterLeft, currentPlayerCharacter, gtime, cooldownJump, lastJump, playerYaccel, playerYspeed, on_ground, jumped, camX, camY)
    pygame.display.update()
    time.tick(120)
