'''

--------------------------------------------------------------------------------------------

                                    ISOMETRIC MINESWEEPER
                                    Author: Bit-Sahil04

--------------------------------------------------------------------------------------------

'''
import sys, os
import pygame
from customColors import customColors as cc
import Minesweeper as ms
from Minesweeper import text_to_screen as tts

if sys.platform in ["win32", "win64"]: os.environ["SDL_VIDEO_CENTERED"] = "1"

pygame.init()
res = (1024, 600)
screen = pygame.display.set_mode(res)
DEBUGGING_MODE = False
bgColor = None
bomb_count = 150

pygame.display.set_caption("Isometric Minesweeper @Bit-Sahil04")


def options(screen):
    global bomb_count, DEBUGGING_MODE
    running = True
    click = False
    BUTTON_WIDTH = res[0] * 0.3
    BUTTON_HEIGHT = res[1] * 0.06
    window_rect = pygame.Surface.get_rect(screen)
    optionsClock = pygame.time.Clock()

    # UI elements
    sliderBox = pygame.rect.Rect(window_rect.right // 1.3 - 20, window_rect.centery + window_rect.centery // 3 + 4,
                                 window_rect.width // 5, BUTTON_HEIGHT)
    sliderBall = pygame.rect.Rect(sliderBox.x, sliderBox.y + BUTTON_HEIGHT // 3, 15, 15)
    sliderLine = pygame.rect.Rect(window_rect.right // 1.3 - 20, sliderBall.centery, window_rect.width // 5, 2)
    toggleBox = pygame.rect.Rect(sliderBox.x, sliderBox.y + BUTTON_HEIGHT * 1.5, BUTTON_WIDTH // 2, BUTTON_HEIGHT)
    toggleRect = pygame.rect.Rect(sliderBox.x + ((BUTTON_WIDTH // 4) * DEBUGGING_MODE),
                                  sliderBox.y + BUTTON_HEIGHT * 1.5, BUTTON_WIDTH // 4, BUTTON_HEIGHT)

    # Buttons
    BACK = pygame.rect.Rect(res[0] // 2.7, res[1] * 0.9, BUTTON_WIDTH, BUTTON_HEIGHT)
    # DEBUG = pygame.rect.Rect(res[0] // 2.7, res[1] * 0.9, BUTTON_WIDTH, BUTTON_HEIGHT)

    mouseHold = False
    sliderBall.centerx = sliderBox.x + bomb_count - 58

    # Draw UI
    screen.fill(bgColor)
    drawTitle(screen)
    while running:
        optionsClock.tick(60)
        ms.maskRect(screen, 0, res[1] // 2, res[0], res[1] // 2, bgColor)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                click = True

        mx, my = pygame.mouse.get_pos()
        if pygame.mouse.get_pressed()[0] == 1 and not click:  # Checking if mouse is held down or not
            mouseHold = True

        if sliderBox.collidepoint(mx, my) and mouseHold:  # Mouse interaction with slider
            if sliderBall.centerx != (mx + sliderBall.width // 2):
                sliderBall.centerx += (mx - sliderBall.centerx) * 0.25
                bomb_count = (sliderBall.x - sliderBox.x) + 57

        if BACK.collidepoint(mx, my):  # go back to main menu
            pygame.draw.rect(screen, cc.BROWN, BACK)
            if click:
                return
        else:
            pygame.draw.rect(screen, cc.AFGAN_TAN, BACK)

        if toggleBox.collidepoint(mx, my) and click:  # Interaction with the Toggle Switch
            DEBUGGING_MODE = not DEBUGGING_MODE
            if DEBUGGING_MODE:
                toggleRect.x = toggleRect.x + toggleRect.width * DEBUGGING_MODE
            else:
                toggleRect.x = toggleBox.x

        if DEBUGGING_MODE:
            pygame.draw.rect(screen, cc.WHITE, sliderBox, 1)

        pygame.draw.rect(screen, cc.WHITE, sliderLine)
        pygame.draw.ellipse(screen, cc.RED, sliderBall)
        tts(screen, bomb_count, sliderBall.centerx, sliderBall.centery - sliderBall.width // 1.5, color=cc.WHITE)

        tts(screen, "Bomb Count:", sliderLine.x - res[0] // 2, sliderLine.y, 20, cc.WHITE)
        tts(screen, " Back ", BACK.centerx, BACK.centery, 20, cc.WHITE)
        tts(screen, "Debugging Mode", toggleBox.x - res[0] // 2, toggleBox.centery, 20, cc.WHITE)

        tts(screen, "ON                  OFF", toggleBox.centerx, toggleBox.centery, 10, color=cc.WHITE)
        pygame.draw.rect(screen, cc.AFGAN_TAN, toggleBox, 1)
        pygame.draw.rect(screen, cc.CRIMSON, toggleRect)

        mouseHold = False
        click = False
        pygame.display.flip()


def button_action(screen, text):
    text = text.lower()
    if text == 'new game':
        ms.game(res, screen, bomb_count, DEBUGGING_MODE)
        mainMenu()
    elif text == 'exit':
        sys.exit()
    elif text == 'options':
        options(screen)
        mainMenu()
    else:
        print('invalid entry')


def drawTitle(screen):
    sfont = pygame.font.Font("assets/fonts/04B_19__.ttf", 50)
    rect_border = pygame.rect.Rect(res[0] // 6 - 29, res[1] // 5 - 21, 725, 100)
    pygame.draw.rect(screen, cc.MAHOGANY, rect_border)
    pygame.draw.rect(screen, cc.GOLD, rect_border, 1)
    # Emulating a "3D shadow" effect by creating copies of text with a slight offset in black color
    tts(screen, "ISOMETRIC MINESWEEPER", res[0] // 2 + 7, res[1] // 4 - 5, 60, cc.BLACK, sfont)
    tts(screen, "ISOMETRIC MINESWEEPER", res[0] // 2 + 6, res[1] // 4 - 3, 60, cc.BLACK, sfont)
    tts(screen, "ISOMETRIC MINESWEEPER", res[0] // 2 + 5, res[1] // 4 - 1, 60, cc.BLACK, sfont)
    tts(screen, "ISOMETRIC MINESWEEPER", res[0] // 2 + 4, res[1] // 4 + 1, 60, cc.BLACK, sfont)
    tts(screen, "ISOMETRIC MINESWEEPER", res[0] // 2 + 3, res[1] // 4 + 2, 60, cc.BLACK, sfont)
    tts(screen, "ISOMETRIC MINESWEEPER", res[0] // 2 + 2, res[1] // 4 + 4, 60, cc.BLACK, sfont)
    tts(screen, "ISOMETRIC MINESWEEPER", res[0] // 2 + 1, res[1] // 4 + 6, 60, cc.BLACK, sfont)
    tts(screen, "ISOMETRIC MINESWEEPER", res[0] // 2, res[1] // 4 + 8, 60, cc.GOLD, sfont)


def mainMenu():
    global bgColor
    global bomb_count
    running = True
    window_rect = pygame.Surface.get_rect(screen)
    mainClock = pygame.time.Clock()
    BUTTON_WIDTH = res[0] * 0.3
    BUTTON_HEIGHT = res[1] * 0.06

    # Buttons
    NEW_GAME = pygame.rect.Rect(window_rect.centerx - (BUTTON_WIDTH / 2),
                                window_rect.centery + BUTTON_HEIGHT * 1.5,
                                BUTTON_WIDTH, BUTTON_HEIGHT)

    OPTIONS = pygame.rect.Rect(window_rect.centerx - (BUTTON_WIDTH / 2),
                               window_rect.centery + BUTTON_HEIGHT * 3.0,
                               BUTTON_WIDTH, BUTTON_HEIGHT)

    EXIT = pygame.rect.Rect(window_rect.centerx - (BUTTON_WIDTH / 2),
                            window_rect.centery + BUTTON_HEIGHT * 4.5,
                            BUTTON_WIDTH, BUTTON_HEIGHT)

    buttons = {"New Game": NEW_GAME, "Options": OPTIONS, "Exit": EXIT}

    click = False

    bgColor = cc.BLUE_STONE
    screen.fill(bgColor)
    drawTitle(screen)

    for button in buttons:
        pygame.draw.rect(screen, cc.AFGAN_TAN, buttons[button])
        tts(screen, button, buttons[button].centerx, buttons[button].centery, 20, color=cc.WHITE)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                click = True

        mx, my = pygame.mouse.get_pos()

        for button in buttons:
            if buttons[button].collidepoint(mx, my):
                highlighted_button = button
                pygame.draw.rect(screen, cc.BROWN, buttons[button])
                if click:
                    button_action(screen, button)
                    # Reset screen
                    screen.fill(bgColor)
                    drawTitle(screen)
            else:
                pygame.draw.rect(screen, cc.AFGAN_TAN, buttons[button])
            tts(screen, button, buttons[button].centerx, buttons[button].centery, 20, color=cc.WHITE)

        click = False
        mainClock.tick(60)
        pygame.display.flip()


mainMenu()
