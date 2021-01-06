import kilobotClass
from math import fabs, sqrt
import random2


# get random int number between -1 and 1
def getRandSpin():
    return random2.randint(-1, 1)

# get random int number between 0 and 255
def getRandColor():
    return random2.randint(0, 255)


# get random int number between 0 and 255
def getRandMotorVal():
    return random2.randint(0, 255)


# get random int number between 0 and 255
def getRandMotorValHalf():
    return random2.randint(0, 127)


def getRandBool():
    return random2.randint(0, 1)


def getRandval():
    return random2.randint(0, 100)


# # check collison between the kilobot and array of kilobots/borders for simple movement
# def checkCollisionLoop(kilobot, kilobots_array_temp, resx, resy, x_temp, y_temp, ):
#     for it in kilobots_array_temp:
#         if kilobot == it:
#             continue
#         if kilobot.checkSingleCollisionPrediction(kilobot.x + x_temp, kilobot.y + y_temp, it.x, it.y):
#             print("Kilobot " + str(it.id) + " collided with a different robot")
#             return True
#     if kilobot.checkWallCollisionPrediction(kilobot.x + x_temp, kilobot.y + y_temp, resx, resy):
#         print("Kilobot " + str(kilobot.id) + " collided with a wall")
#         return True
#
#
# # check collison between the kilobot and array of kilobots/borders for teleport
# def checkCollisionLoop_tp(kilobot, kilobots_array_temp, resx, resy, x_tp, y_tp):
#     for it in kilobots_array_temp:
#         if kilobot == it:
#             continue
#         if kilobot.checkSingleCollisionPrediction(x_tp, y_tp, it.x, it.y):
#             print("Kilobot " + str(it.id) + " collided with a different robot")
#             return True
#     if kilobot.checkWallCollisionPrediction(x_tp, y_tp, resx, resy):
#         print("Kilobot " + str(kilobot.id) + " collided with a wall")
#
#         return True
#
#
# # check collison between the kilobot and array of kilobots/borders for rotation movement
# def checkCollisionLoop_Rotate(kilobot, kilobots_array_temp, resx, resy, forward, fi_temp):
#     for it in kilobots_array_temp:
#         if kilobot == it:
#             continue
#         if kilobot.checkCollisionPrediction_Rotaton(it.x, it.y, forward, fi_temp):
#             print("Kilobot " + str(it.id) + " collided with a different robot")
#             return True
#     if kilobot.checkWallCollisionPrediction_Rotaton(resx, resy, forward, fi_temp):
#         print("Kilobot " + str(kilobot.id) + " collided with a wall")
#         return True


# check collison between the kilobot and array of kilobots/borders for Motors movement
def checkCollisionLoop_Motors(kilobot, kilobots_array_temp, resx, resy, fi_temp, precison):
    for it in kilobots_array_temp:
        if kilobot == it:
            continue
        # if kilobot.checkCollisionPrediction_Motors(it.x, it.y, fi_temp, precison):
        #     print("Kilobot " + str(it.id) + " collided with a different robot")
        #     return True
    if kilobot.checkWallCollisionPrediction_Motors(resx, resy, fi_temp, precison):
        # print("Kilobot " + str(kilobot.id) + " collided with a wall")
        return True


# def kilobotsMovement(enableTag, kilobotsArray, FoodArray, resx, resy, screen):
#     if enableTag:
#
#         closer = True
#         for it in kilobotsArray:
#             closestFood = it.findClosestFood()
#             M1 = 255
#             M2 = 255
#             if closestFood is not ValueError and len(it.inIRRangeFoodID) == len(it.foodID_last):
#                 if len(it.foodID_last) > 0:
#                     if not checkCollisionLoop_Motors(it, FoodArray, resx, resy, (M1 - M2) * 0.001) and not checkCollisionLoop_Motors(it, FoodArray, resx, resy, M1 * 0.001):
#                         if it.foodID_last[closestFood][1] >= it.inIRRangeFoodID[closestFood][1]:
#                             closer = True
#                         else:
#                             closer = False
#                         if closer:
#                             if not checkCollisionLoop_Motors(it, kilobotsArray, resx, resy, (M1 - M2) * 0.001):
#                                 it.MotorsMoveKilobot(M1, M2)
#
#                         else:
#                             for k in range(0, 1):
#                                 if not checkCollisionLoop_Motors(it, kilobotsArray, resx, resy, M1 * 0.001):
#                                     it.MotorsMoveKilobot(M1, 0)
#
#
#                     else:
#                         it.changeColor(255, 0, 0)
#             it.drawKilobot(screen)

def kilobotsMovement(enableTag, kilobotsArray, FoodArray, resx, resy, screen):
    if enableTag:

        closer = True
        it1 = 0
        for it in kilobotsArray:
            it1 = it1 + 1
            # find closest food in range
            closestFood = it.findClosestFood()
            M1 = getRandMotorVal()
            M2 = getRandMotorVal()
            val = getRandBool()
            if closestFood is None:

                if not checkCollisionLoop_Motors(it, kilobotsArray, resx, resy, (M1 - M2) * 0.01, 10):
                    it.MotorsMoveKilobot(M1, M2, 0.5)
                    it.collision = False
                else:
                    it.collision = True
            if it.collision:
                if not checkCollisionLoop_Motors(it, kilobotsArray, resx, resy, M1 * 0.01, 0.01):
                    it.MotorsMoveKilobot(M1, 0, 0.1)

                else:
                    kilobotsArray.pop(it1 - 1)




            # food detected, start moving to food
            else:
                M1 = 255
                M2 = 255
                if closestFood is not ValueError and len(it.inIRRangeFoodID) == len(it.foodID_last):
                    if len(it.foodID_last) > 0:
                        # chceck if food was found
                        if not checkCollisionLoop_Motors(it, FoodArray, resx, resy,
                                                         (M1 - M2) * 0.001, 1) and not checkCollisionLoop_Motors(it,
                                                                                                                 FoodArray,
                                                                                                                 resx,
                                                                                                                 resy,
                                                                                                                 M1 * 0.01,
                                                                                                                 1):
                            # check if kilobot is getting closer to food
                            if it.foodID_last[closestFood][1] >= it.inIRRangeFoodID[closestFood][1]:
                                closer = True
                            else:
                                closer = False

                            # move forward if getting closer
                            if closer:
                                if not checkCollisionLoop_Motors(it, kilobotsArray, resx, resy, (M1 - M2) * 0.01, 1):
                                    it.MotorsMoveKilobot(M1, M2, 0.5)
                                    print("X: " + str(it.x) + " Y: " + str(it.y))
                                    it.collision = False
                                else:
                                    it.collision = True

                            # rotate if getting closer
                            else:
                                for k in range(0, 4):
                                    if not checkCollisionLoop_Motors(it, kilobotsArray, resx, resy, M1 * 0.01, 0.01):
                                        it.MotorsMoveKilobot(M1, 0, 0.1)
                                        it.collision = False
                                    else:
                                        it.collision = True
                                    print("X: " + str(it.x) + " Y: " + str(it.y))

                            if it.collision:
                                kilobotsArray.pop(it1 - 1)

                        # if food was found change color
                        else:
                            it.changeColor(255, 0, 0)
            it.drawKilobot(screen)


def AIrotateleft(enableTag, kilobotsArray, id, screen):
    if enableTag:
        M1 = 255
        M2 = 255
        kilobotsArray[id].MotorsMoveKilobot(M1, 0, 2)
        # kilobotsArray[id].rotateKilobot(20)
        # kilobotsArray[id].drawKilobot(screen)


def AIrotateright(enableTag, kilobotsArray, id, screen):
    if enableTag:
        M1 = 255
        M2 = 255
        kilobotsArray[id].MotorsMoveKilobot(0, M2, 2)
        # kilobotsArray[id].rotateKilobot(-20)
        # kilobotsArray[id].drawKilobot(screen)


def AIMoveFront(enableTag, kilobotsArray, id, screen):
    if enableTag:
        M1 = 255
        M2 = 255
        kilobotsArray[id].MotorsMoveKilobot(M1, M2, 2)
        # kilobotsArray[id].drawKilobot(screen)


def AIMoveStop(enableTag, kilobotsArray, id, screen):
    if enableTag:
        M1 = 0
        M2 = 0
        kilobotsArray[id].MotorsMoveKilobot(M1, M2, 2)
        # kilobotsArray[id].drawKilobot(screen)


def AIDynamicMovementL1(enableTag, kilobotsArray, id, screen):
    if enableTag:
        M1 = 255
        M2 = 51
        kilobotsArray[id].MotorsMoveKilobot(M1, M2, 2)
        kilobotsArray[id].drawKilobot(screen)


def AIDynamicMovementL2(enableTag, kilobotsArray, id, screen):
    if enableTag:
        M1 = 204
        M2 = 102
        kilobotsArray[id].MotorsMoveKilobot(M1, M2, 0.5)
        kilobotsArray[id].drawKilobot(screen)


def AIDynamicMovementM(enableTag, kilobotsArray, id, screen):
    if enableTag:
        M1 = 153
        M2 = 153
        kilobotsArray[id].MotorsMoveKilobot(M1, M2, 1)
        kilobotsArray[id].drawKilobot(screen)


def AIDynamicMovementR1(enableTag, kilobotsArray, id, screen):
    if enableTag:
        M1 = 51
        M2 = 255
        kilobotsArray[id].MotorsMoveKilobot(M1, M2, 2)
        kilobotsArray[id].drawKilobot(screen)


def AIDynamicMovementR2(enableTag, kilobotsArray, id, screen):
    if enableTag:
        M1 = 102
        M2 = 204
        kilobotsArray[id].MotorsMoveKilobot(M1, M2, 0.5)
        kilobotsArray[id].drawKilobot(screen)


def RandomMovement(enableTag, kilobotsArray, resx, resy):
    if enableTag:

        it1 = 0
        for it in kilobotsArray:

            M1 = getRandMotorVal()
            M2 = getRandMotorVal()

            if not checkCollisionLoop_Motors(it, kilobotsArray, resx, resy, (M1 - M2) * 0.01, 10):
                it.MotorsMoveKilobot(M1, M2, 0.5)
                it.collision = False
            else:
                it.collision = True
            if it.collision:
                if not checkCollisionLoop_Motors(it, kilobotsArray, resx, resy, M1 * 0.01, 0.01):
                    it.MotorsMoveKilobot(M1, 0, 0.1)

                else:
                    kilobotsArray.pop(it1 - 1)
            it1 += 1


def RandomMovement_test(enableTag, kilobotsArray, resx, resy, V):
    if enableTag:

        for it in kilobotsArray:

            M1, M2 = it.GetMotorsValue()

            if not checkCollisionLoop_Motors(it, kilobotsArray, resx, resy, (M1 - M2) * 0.01, 10):
                it.MotorsMoveKilobot(M1, M2, V)
                it.collision = False
            else:
                it.collision = True
            if it.collision:
                if not checkCollisionLoop_Motors(it, kilobotsArray, resx, resy, M1 * 0.01, 0.01):
                    it.MotorsMoveKilobot(M1, 0, V)

                else:
                    it.BounceIfWallCollision(resx, resy)
            it.StoreMotorsValue(M1, M2)
