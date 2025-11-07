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
window = pygame.display.set_mode((width, height))
lvlwindow=pygame.display.set_mode((width,height))
pygame.display.set_caption("Space runner")
pygame.mouse.set_visible(False)

background = pygame.image.load("graphics/sun2dnew.png").convert()
play_Button = pygame.image.load("graphics/playButton.png").convert_alpha()
settings_Button = pygame.image.load("graphics/settingsButton.png").convert_alpha()
quit_Button = pygame.image.load("graphics/quitButton.png").convert_alpha()
cursor = pygame.image.load("graphics/cursor2d.png").convert_alpha()
cursor_mask = pygame.mask.from_surface(cursor)
quit_Button_mask = pygame.mask.from_surface(quit_Button)
settings_Button_mask = pygame.mask.from_surface(settings_Button)
play_Button_mask = pygame.mask.from_surface(play_Button)

playAudio = False
lastOnButton = False
NowOnButton = False
def lvlScreen():
    while True:
     for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()



def menu(playAudio, lastOnButton, NowOnButton):
 while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()    
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
                lvlScreen()
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
        return playAudio, lastOnButton, NowOnButton

    playAudio, lastOnButton, NowOnButton = menu(playAudio, lastOnButton, NowOnButton)
pygame.display.update()
time.tick(120)
