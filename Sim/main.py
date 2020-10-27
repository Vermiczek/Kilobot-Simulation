from math import fabs, sqrt

import pygame
import kilobotClass
from button import button

# inicjalizacja biblioteki
pygame.init()


# rysowanie kółek
def drawCircle(pos, r, g, b):
    pygame.draw.circle(screen, (r, g, b), pos, 20)


def checkPlacementCollision(array, X, Y):

    for itr in array:
        xDif = fabs(X-itr.x)
        yDif = fabs(Y-itr.y)
        Dif = sqrt(xDif**2+yDif**2)
        if Dif < 40:
            return True
    return False

def reddrawWindow():
    screen.fill((255,255,255))
    resetButton.draw(screen, (0,0,0))
    startButton.draw(screen, (0,0,0))

resx = 800
resy= 600
# tworzenie ekranu
screen = pygame.display.set_mode((resx, resy))

# deklaracja tablicy kilobotow
kilobots = []

#tworzenie przycisku reset
resetButton = button((0,255,0), 0, 550, 100, 50, 'Reset')
startButton = button((0,255,0), 120, 550, 100, 50, 'Start')

# glowna pętla
running = True
while running:
    reddrawWindow()
    #screen.fill((255, 255, 255))

    for it in kilobots:
        position = (it.x, it.y)
        drawCircle(position, it.r, it.g, it.b)

    for event in pygame.event.get():
        pos = pygame.mouse.get_pos()

        if event.type == pygame.QUIT:
            running = False
        if len(kilobots) <= 20:
            if event.type == pygame.MOUSEBUTTONDOWN:
                mPosX, mPosY = pygame.mouse.get_pos()
                if (mPosX > 20) & (mPosY >20) & (mPosX < (resx - 70)) & (mPosY < (resy -70)):

                    if not checkPlacementCollision(kilobots, mPosX, mPosY):
                        kilobots.append(kilobotClass.Kilobot(mPosX, mPosY, 255, 0, 0))

        if event.type == pygame.MOUSEBUTTONDOWN:
            if resetButton.isOver(pos):
                print('clicked reset button')
                kilobots.clear()
            if startButton.isOver(pos):
                print('clicked start button')

    pygame.display.update()
