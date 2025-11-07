import pygame
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
    #print(choice_Order)

def scale_button(button_img, button_rect, hovered):
    if hovered:
        scale_factor = 1.1
        new_size = (int(button_rect.width * scale_factor), int(button_rect.height * scale_factor))
        scaled_img = pygame.transform.scale(button_img, new_size)
        scaled_rect = scaled_img.get_rect(center=button_rect.center)
        return scaled_img, scaled_rect
    else:
        return button_img, button_rect

width = 1920
height = 1080
relative_Button_position = 200
play_Button_position = 300
game_mode="menu"
window = pygame.display.set_mode((width, height))
lvlwindow=pygame.display.set_mode((width,height))
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


cursor_mask = pygame.mask.from_surface(cursor)
quit_Button_mask = pygame.mask.from_surface(quit_Button)
settings_Button_mask = pygame.mask.from_surface(settings_Button)
play_Button_mask = pygame.mask.from_surface(play_Button)
back_Button_mask = pygame.mask.from_surface(back_Button)

levels1_image_mask = pygame.mask.from_surface(levels1_image)
levels2_image_mask = pygame.mask.from_surface(levels2_image)
levels3_image_mask = pygame.mask.from_surface(levels3_image)
levels4_image_mask = pygame.mask.from_surface(levels4_image)
levels5_image_mask = pygame.mask.from_surface(levels5_image)


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

    play_hovered = play_Button_mask.overlap(cursor_mask, (cursor_pos[0] - play_Button_rect.x, cursor_pos[1] - play_Button_rect.y))
    settings_hovered = settings_Button_mask.overlap(cursor_mask, (cursor_pos[0] - settings_Button_rect.x, cursor_pos[1] - settings_Button_rect.y))
    quit_hovered = quit_Button_mask.overlap(cursor_mask, (cursor_pos[0] - quit_Button_rect.x, cursor_pos[1] - quit_Button_rect.y))

    play_img, play_rect = scale_button(play_Button, play_Button_rect, play_hovered)
    settings_img, settings_rect = scale_button(settings_Button, settings_Button_rect, settings_hovered)
    quit_img, quit_rect = scale_button(quit_Button, quit_Button_rect, quit_hovered)

    if quit_hovered:
        NowOnButton = True
        if pygame.mouse.get_pressed()[0]:
            pygame.quit()
        elif not lastOnButton:
            lastOnButton = True
            playAudio = True
            menuClicksAudio()
    elif settings_hovered:
        NowOnButton = True
        if pygame.mouse.get_pressed()[0]:
            pygame.quit()
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
    
    levels_image_rect = levels_image.get_rect()
    levels_image_rect.center = (width / 2, 220)
    levels1_image_rect = levels_image.get_rect()
    levels1_image_rect.center = (280, height/2)
    levels2_image_rect = levels_image.get_rect()
    levels2_image_rect.center = (530, height/2)
    levels3_image_rect = levels_image.get_rect()
    levels3_image_rect.center = (780, height/2)
    levels4_image_rect = levels_image.get_rect()
    levels4_image_rect.center = (1030, height/2)
    levels5_image_rect = levels_image.get_rect()
    levels5_image_rect.center = (1280, height/2)
    back_Button_rect = back_Button.get_rect()
    back_Button_rect.center = (340, 900)

    levels1_image_hovered = levels1_image_mask.overlap(cursor_mask, (cursor_pos[0] - levels1_image_rect.x, cursor_pos[1] - levels1_image_rect.y))
    levels2_image_hovered = levels2_image_mask.overlap(cursor_mask, (cursor_pos[0] - levels2_image_rect.x, cursor_pos[1] - levels2_image_rect.y))
    levels3_image_hovered = levels3_image_mask.overlap(cursor_mask, (cursor_pos[0] - levels3_image_rect.x, cursor_pos[1] - levels3_image_rect.y))
    levels4_image_hovered = levels4_image_mask.overlap(cursor_mask, (cursor_pos[0] - levels4_image_rect.x, cursor_pos[1] - levels4_image_rect.y))
    levels5_image_hovered = levels5_image_mask.overlap(cursor_mask, (cursor_pos[0] - levels5_image_rect.x, cursor_pos[1] - levels5_image_rect.y))
    back_Button_hovered =   back_Button_mask.overlap(cursor_mask, (cursor_pos[0] - back_Button_rect.x, cursor_pos[1] - back_Button_rect.y))



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
        elif not lastOnButton:
            lastOnButton = True
            playAudio = True
            menuClicksAudio()
    elif levels3_image_hovered:
        NowOnButton = True
        if pygame.mouse.get_pressed()[0]:
            pygame.quit()
        elif not lastOnButton:
            lastOnButton = True
            playAudio = True
            menuClicksAudio()
    elif levels4_image_hovered:
        NowOnButton = True
        if pygame.mouse.get_pressed()[0]:
            pygame.quit()
        elif not lastOnButton:
            lastOnButton = True
            playAudio = True
            menuClicksAudio()
    elif levels5_image_hovered:
        NowOnButton = True
        if pygame.mouse.get_pressed()[0]:
            pygame.quit()
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
def lvl1(playAudio, lastOnButton, NowOnButton, game_mode):
    cursor_pos = pygame.mouse.get_pos()
    quit_Button_rect = quit_Button.get_rect()
    quit_Button_rect.center = (width / 2, 2 * relative_Button_position + play_Button_position)
    settings_Button_rect = settings_Button.get_rect()
    settings_Button_rect.center = (width / 2, relative_Button_position + play_Button_position)
    play_Button_rect = play_Button.get_rect()
    play_Button_rect.center = (width / 2, play_Button_position)

    play_hovered = play_Button_mask.overlap(cursor_mask, (cursor_pos[0] - play_Button_rect.x, cursor_pos[1] - play_Button_rect.y))
    settings_hovered = settings_Button_mask.overlap(cursor_mask, (cursor_pos[0] - settings_Button_rect.x, cursor_pos[1] - settings_Button_rect.y))
    quit_hovered = quit_Button_mask.overlap(cursor_mask, (cursor_pos[0] - quit_Button_rect.x, cursor_pos[1] - quit_Button_rect.y))

    play_img, play_rect = scale_button(play_Button, play_Button_rect, play_hovered)
    settings_img, settings_rect = scale_button(settings_Button, settings_Button_rect, settings_hovered)
    quit_img, quit_rect = scale_button(quit_Button, quit_Button_rect, quit_hovered)

    if quit_hovered:
        NowOnButton = True
        if pygame.mouse.get_pressed()[0]:
            pygame.quit()
        elif not lastOnButton:
            lastOnButton = True
            playAudio = True
            menuClicksAudio()
    elif settings_hovered:
        NowOnButton = True
        if pygame.mouse.get_pressed()[0]:
            pygame.quit()
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
while True:
    mouse_pos = pygame.mouse.get_pos()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()

    if game_mode == "menu":
        playAudio, lastOnButton, NowOnButton, game_mode = menu(playAudio, lastOnButton, NowOnButton, game_mode)
    elif game_mode == "Levels":
        playAudio, lastOnButton, NowOnButton, game_mode = lvlScreen(playAudio, lastOnButton, NowOnButton, game_mode)
    elif game_mode == "lvl1":
        playAudio, lastOnButton, NowOnButton, game_mode = lvl1(playAudio, lastOnButton, NowOnButton, game_mode)


    pygame.display.update()
    time.tick(120)
