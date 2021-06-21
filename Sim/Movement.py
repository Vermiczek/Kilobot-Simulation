import kilobotClass
from math import fabs, sqrt
import random2
import matplotlib.pyplot as plt
import numpy as np
import BasicFunc
import numpy as np
import scikit

changedTarget = 0
lostTarget = 0


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




def kilobotsMovementSnake(enableTag, kilobotsArray):
    """
    Makes kilobots search for their target and move in a line (line movement)
    :param: enableTag: tag deciding on whether the simulation is running
    :param: kilobotsArray: array of existing kilobots
    :return: none
    """
    global lostTarget
    if enableTag:

        it1 = 0
        for it in kilobotsArray:
            it1 = it1 + 1
            # find closest food in range
            it.targetBotID = it.id
            it.found = 0
            it.findLowerIDBot()

            # decides on whether the kilobot's target is in his range
            for itr2 in it.inIRRangeKilobotID:
                if itr2[0] == it.targetBotID:
                    it.found = 1
                    break

            if it.found == 0:
            # resets kilobot data so it doesn't bug out
                it = resetKilobotData(it)
                randomMovement(it)
            else:
            # regulates kilobot's orientation to direct him towards his target as perfectly as possible
                speedModifier = distanceAndSpeed(it.distanceToTarget)
                spinModifier = it.spinCounter / 100
                M = 255 * speedModifier
                it.spinmodlist.append(it.spinCounter)
                if it.found == 1:
                    for itr2 in it.inIRRangeKilobotID:
                        if itr2[0] == it.targetBotID:
                            #calculate the speed
                            it.speedTowardsTarget = it.distanceToTarget - itr2[1]
                    if it.speedTowardsTarget < it.lastSpeedTowardsTarget:
                        it.spin = -it.spin
                        it.detectOscilations=it.detectOscilations + 2
                        oscilationsStala = 30
                        if it.detectOscilations >= oscilationsStala:
                            it.detectOscilations = oscilationsStala
                        if it.detectOscilations >= 30:
                            it.alterSpinCounter(-20)
                    else:
                        it.detectOscilations = it.detectOscilations -1
                        if it.detectOscilations < 0:
                            it.detectOscilations = 0
                        it.alterSpinCounter(10)
                    if it.spin == -1:
                        M1 = M * spinModifier
                        M2 = (M - M1)
                    else:
                        M2 = M * spinModifier
                        M1 = (M - M2)

                    it.MotorsMoveKilobot(M1, M2, 0.5)

                    #calculate ideal fi and make measurements1
                    it = allMeasurements(kilobotsArray, it, M1, M2, M)


                    it.lastSpeedTowardsTarget = it.speedTowardsTarget
                    for itr2 in it.inIRRangeKilobotID:
                        if itr2[0] == it.targetBotID:
                            it.distanceToTarget = itr2[1]
            print(it.speedTowardsTarget)

def resetKilobotData(kilobot):
    """
        Resets control data of a kilobot
        :param: kilobot: object of kilobot class
        :return: kilobot: updated object of kilobot class
        """
    kilobot.distanceToTarget = 0
    kilobot.lastSpeedTowardsTarget = 0
    kilobot.speedTowardsTarget = 0
    kilobot.targetBotID
    return kilobot

def allMeasurements(kilobotsArray, it, M1, M2, M):
    """
            Takes all measurements neccessary for line movement research
            :param: kilobot: object of kilobot class
            :return: it: updated object of kilobot class with measurements taken
            """
    for itr3 in kilobotsArray:
        if itr3.id == it.targetBotID:
            x1 = itr3.x - it.x
            y1 = itr3.y - it.y
            if y1 == 0:
                y1 = 0.1

            tang = x1 / y1
            if (itr3.x < it.x) & (itr3.y > it.y):
                wantedFi = np.arctan(tang)
                wantedFi = wantedFi * (180 / 3.14)
            if (itr3.x > it.x) & (itr3.y > it.y):
                wantedFi = np.arctan(tang)
                wantedFi = wantedFi * (180 / 3.14)
            if (itr3.x < it.x) & (itr3.y < it.y):
                wantedFi = np.arctan(tang)
                wantedFi = -180 + wantedFi * (180 / 3.14)
            if (itr3.x > it.x) & (itr3.y < it.y):
                wantedFi = np.arctan(tang)
                wantedFi = -(-180 - wantedFi * (180 / 3.14))

    uchybtemp = wantedFi - it.fi
    uchyb = sqrt(uchybtemp * uchybtemp)
    spd = it.speedTowardsTarget * 120
    it.dttList.append(it.distanceToTarget)
    it.uchybList.append(uchyb)
    it.sttList.append(spd)
    it.wantedFiList.append(wantedFi)
    it.orientationList.append(it.fi)
    it.m1list.append(M1)
    it.mlist.append(M)
    it.m2list.append(M2)
    return it

def randomMovement(kilobot):
    """
              Makes kiilobot move randomly (line movement)
              :param: kilobot: object of kilobot class
              :return: none
              """
    rand = random2.randint(0, 1)

    if rand == 0:
        m1 = 255
        m2 = 0
    else:
        m1 = 0
        m2 = 255
    if len(kilobot.inIRRangeKilobotID) is not 0:
        kilobot.MotorsMoveKilobot(0.5 * m1, 0.5 * m2, 0.5)
    elif len(kilobot.inIRRangeKilobotID) is 0:
        kilobot.MotorsMoveKilobot(m1, m2, 0.5)

def distanceAndSpeed(distance):
    """
            Adjusts kilobot's speed with distance to his target (line movement)
            :param: distance: distance to kilobot's target
            :return: Modifier: modifier used to alter the speed of a kilobot
            """
    if distance > 100:
        Modifier = 1
    elif distance < 30:
        Modifier = 0
    else:
        Modifier = distance / 100
    return Modifier


def kilobotsFoodFindingMovement(enableTag, kilobotsArray, FoodsArray, screen, time):
    """
        Movement function of food finding algorithm
        :param: enableTag: Flag which enables movement
        :param: kilobotsArray: Array of existing Kilobots
        :param: FoodsArray: Array of existing Foods
        :param: screen: Physical space
        :param: time: Objects which contains simulation time
        :return: none:
    """
    #if movement flag is true
    if enableTag:
        it1 = 0
        # for each kilobot in kilobotsArray
        for it in kilobotsArray:
            it1 = it1 + 1
            # find closest food in range
            closestFood = it.findClosestFood()
            #gets random motors value in range 0-255
            M1 = getRandMotorVal()
            M2 = getRandMotorVal()
            #if there is no food in range - random movement
            if closestFood is None:
                it.MotorsMoveKilobot(M1, M2, 0.5) #moves kilobots
                if time >=5 and time%5==0 and time%10!=0: #time condition, if true then adds additional movement randomness
                    M1 = getRandMotorValHalf() #gets random motor value in range 0-127
                    it.MotorsMoveKilobot(M1, 0, 0.5) #moves kilobots
                elif time >=10 and time%10==0: #time condition, if true then adds additional movement randomness
                    M2 = getRandMotorValHalf() #gets random motor value in range 0-127
                    it.MotorsMoveKilobot(0, M2, 0.5) #moves kilobots
            # food detected, start moving to food
            else:
                M1 = 255 #Sets M1 activation value to 255
                M2 = 255 #Sets M2 activation value to 255
                # chceck if food was found
                if closestFood is not ValueError and len(it.inIRRangeFoodID) == len(it.foodID_last):
                    if len(it.foodID_last) > 0 and not it.inIRRangeFoodID[closestFood][1] < 35: #checks if distance to food is greater than 35 units
                        # check if kilobot is getting closer to food
                        if it.foodID_last[closestFood][1] >= it.inIRRangeFoodID[closestFood][1]:
                            closer = True #if kilbot is getting closer to food - sets closer flag to True
                        else:
                            closer = False
                        # move forward if getting closer
                        if closer:
                            it.MotorsMoveKilobot(M1, M2, 0.5) #moves kilobot in straight line
                        # rotate if getting closer
                        else:
                            for k in range(0, 8):
                                it.MotorsMoveKilobot(M1, 0, 0.5) #moves kilobots in an arc
                        # if food was found change color and stop
                    else :
                        it.changeColor(255, 0, 0)
                        it.body.velocity = (0, 0)
            it.drawKilobot(screen)


def FuzzyFoodMovement(enableTag, kilobotsArray, screen, time):
    """
        Movement function of fuzzy-based food finding algorithm
        :param: enableTag: Flag which enables movement
        :param: kilobotsArray: Array of existing Kilobots
        :param: screen: Physical space
        :param: time: Objects which contains simulation time
        :return: none:
    """
    #if movement flag is true
    if enableTag:
        it1 = 0
        # for each kilobot in kilobotsArray
        for it in kilobotsArray:
            it1 = it1 + 1
            # find closest food in range
            closestFood = it.findClosestFood()
            #gets random motor value in range 0-255
            M1 = getRandMotorVal()
            M2 = getRandMotorVal()
            #if there is no food in range - random movement
            if closestFood is None:
                it.MotorsMoveKilobot(M1, M2, 0.5)
                if time >=5 and time%5==0 and time%10!=0: #time condition, if true then adds additional movement randomness
                    M1 = getRandMotorValHalf() #gets random motor value in range 0-127
                    it.MotorsMoveKilobot(M1, 0, 0.5)#rotates kilobots
                elif time >=10 and time%10==0: #time condition, if true then adds additional movement randomness
                    M2 = getRandMotorValHalf() #gets random motor value in range 0-127
                    it.MotorsMoveKilobot(0, M2, 0.5)#rotates kilobots
            # food detected, start moving to food
            else:
                M1 = 255 #Sets M1 activation value to 255
                # chceck if food was found
                if closestFood is not ValueError and len(it.inIRRangeFoodID) == len(it.foodID_last):
                    if len(it.foodID_last) > 0 and not it.inIRRangeFoodID[closestFood][1] <= 35: #checks if distance to food is greater than 35 units
                            # check if kilobot is getting closer to food
                            if it.foodID_last[closestFood][1] >= it.inIRRangeFoodID[closestFood][1]:
                                closer = True #if kilbot is getting closer to food - sets closer flag to True
                            else:
                                closer = False

                            if closer:
                                prev_distance = int(it.foodID_last[closestFood][1] * 100) #calculates prev_distance value to pass it to fuzzy function
                                distance = int(it.inIRRangeFoodID[closestFood][1] * 100) #calculates distance value to pass it to fuzzy function

                                M2_val = round(scikit.scifuzz(distance, prev_distance)) #Fuzzy-based function calculates value of M2 motor
                                it.MotorsMoveKilobot(M1, M2_val, 0.5)#moves kilobots
                        # if food was found change color and stop
                    else:
                            it.changeColor(255, 0, 0)
                            it.body.velocity = (0, 0)
            it.drawKilobot(screen)

def distanceAndSpeedFuzzyLogic(distance):
    if distance > 100:
        Modifier = 1
    elif distance < 30:
        Modifier = 0
    else:
        Modifier = distance / 100
    return Modifier

#######################################################################################

def kilobotPIDmovement(enableTag, kilobot, screen, Ts, distnace):
    """
        moves kilobots using PID/PD/PI regulators
        :param enableTag: flag to enable global movment
        :param kilobot: object that contains informations about kilobot
        :param screen: object that contains informations about Pygame simulation
        :param Ts: sample time
        :param distnace: input distance to regulate movement
        :return: error and distance
    """

    # check if movement in simulation is enabled
    if enableTag:

        # check if movement is enabled
        if kilobot.enableMovment == True:

            # find closest kilobot
            closestKilobot = kilobot.findClosestKilobot()

            # check if kilobot has data to start moving
            if closestKilobot is not ValueError and len(kilobot.inIRRangeKilobotID) > 0 and len(
                    kilobot.kilobotID_last) > 0:

                # try to get distance to closest kilobot
                try:
                    val = kilobot.inIRRangeKilobotID[closestKilobot][1]
                except IndexError:
                    val = distnace

#######################################################################################################################
# uncomment part of code to choose regulator: PID, PD, PI

                # PID regulator
                #PIDval = kilobot.calcPID(distnace, val, 250, 120, 167, 255, 0,Ts)

                # PD regulator
                #PIDval = kilobot.calcPD(distnace, val, 500,  40, 255, 0,Ts)

                #PI regulator
                PIDval = kilobot.calcPI(distnace, val, 18, 62.5,  255, 0,Ts)

                # error = 40 - kilobot.inIRRangeFoodID[closestFood][1]

                # settig new value for Motor M2
                kilobot.MotorsMoveKilobot_older(127, PIDval, 0.5)

                # print(PIDval)
                kilobot.drawKilobot(screen)
                return distnace-val,val
                # return error


def kilobotPIDmovement_tunning(enableTag, kilobot, screen, Ts, distnace):
    """
        moves kilobots using PID/PD/PI regulators
        Tuning version
        :param enableTag: flag to enable global movment
        :param kilobot: object that contains informations about kilobot
        :param screen: object that contains informations about Pygame simulation
        :param Ts: sample time
        :param distnace: input distance to regulate movement
        :return: None
    """
    # check if movement in simulation is enabled
    if enableTag:

        # find closest kilobot
        closestFood = kilobot.findClosestFood()

        if closestFood is not ValueError and len(kilobot.inIRRangeFoodID) > 0 and len(kilobot.foodID_last) > 0:
            P, I, D = kilobot.getPID()
            PIDval = kilobot.calcPID(distnace, kilobot.inIRRangeFoodID[closestFood][1], P, I, D, 255, 0,
                                     Ts)

            # settig new value for Motor M2
            kilobot.MotorsMoveKilobot_learn(127, PIDval, 0.5)

            # print(PIDval)
            kilobot.drawKilobot(screen)



def kilobotNeuralmovement(enableTag, kilobot, screen, value):
    """
        moves kilobots using neural regulator
        :param enableTag: flag to enable global movment
        :param kilobot: object that contains informations about kilobot
        :param screen: object that contains informations about Pygame simulation
        :param value: output value from NN that controls motor M2
        :return: None
    """
    # check if movement in simulation is enabled
    if enableTag:

        # check if kilobot has enabled movement
        if kilobot.enableMovment == True:

            # Normalization
            if value == 0:
                Motorval = 127
            if value == 1:
                Motorval = 255
            if value == -1:
                Motorval = 0

            # settig new value for Motor M2
            kilobot.MotorsMoveKilobot_older(127, Motorval, 0.5)


            kilobot.drawKilobot(screen)



def kilobotNeuralmovement_learning(enableTag, kilobot, screen, value):
    """
        moves kilobots using neural regulator
        learning version
        :param enableTag: flag to enable global movment
        :param kilobot: object that contains informations about kilobot
        :param screen: object that contains informations about Pygame simulation
        :param value: output value from NN that controls motor M2
        :return: None
    """

    # check if movement in simulation is enabled
    if enableTag:

        # Normalization
        if value == 0:
            Motorval = 127
        if value == 1:
            Motorval = 255
        if value == -1:
            Motorval = 0

        # option for 127 outputs of NN
        # Motorval=value*2

        # settig new value for Motor M2
        kilobot.MotorsMoveKilobot_older(127, Motorval, 0.1)

        kilobot.drawKilobot(screen)



########################################################################################################################

