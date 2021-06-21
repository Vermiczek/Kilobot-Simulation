from cmath import sqrt
from math import fabs, pi, sin, cos, degrees, radians, exp
import pymunk
import BasicFunc

import pygame


def drawKilobots(kilobotArray, screen):
    for it in kilobotArray:
        it.drawKilobot(screen)


def drawFoods(kilobotArray, screen):
    for it in kilobotArray:
        it.drawFood(screen)


class Kilobot:

    def __init__(self, id, x, y, fi, r, g, b, radius):
        """
            Constructor of Kilobot class
            :param: self
            :param: id: Kilobots ID
            :param: x: Kilobots position (x)
            :param: y: Kilobots position (y)
            :param: fi: Kilobots orientation [0-360deg]
            :param: r: Kilobots RGBs r value [0-255]
            :param: g: Kilobots RGBs g value [0-255]
            :param: b: Kilobots RGBs b value [0-255]
            :param: radius: Kilobots radius
            :return: none
        """
        self.id = id
        self.index = id
        self.x = x
        self.y = y
        self.r = r
        self.g = g
        self.b = b
        self.fi = fi
        self.radius = radius
        ############################
        # detection of other kilobots
        self.inIRRangeKilobotID = []
        self.inIRRangeFoodID = []
        ############################
        # #front head
        self.front_x = x
        self.front_y = y + radius - 2
        self.front_radius = radius - 13
        self.front_r = 0
        self.front_g = 0
        self.front_b = 255
        ############################
        self.V = 0.5
        self.Fitness = 0
        ############################
        # PID
        self.pam = 0.0
        self.pamUchyb = 0.0
        self.P = 0
        self.I = 0
        self.D = 0
        self.avg_error = 0
        ############################
        #   physics engine
        self.body = pymunk.Body()
        self.body.position = (self.x, self.y)
        self.shape = pymunk.Circle(self.body, self.radius)
        self.found = 0
        self.shape.friction = 0.7
        self.shape.mass = 1
        ############################
        # snake movement
        self.spin = 1
        self.speedTowardsTarget = 0
        self.lastSpeedTowardsTarget = 0
        self.targetBotID = self.id
        self.distanceToTarget = 0
        self.followed = 0
        self.newTarget = 0
        self.lostTarget = 0
        self.previousTarget = self.id
        self.spinCounter = 100
        self.orientationList = []
        self.wantedFiList = []
        self.uchybList = []
        self.sttList = []
        self.dttList = []
        self.m1list = []
        self.m2list = []
        self.mlist = []
        self.spinmodlist = []
        self.detectOscilations = 0
        ####################################################################
        #creating shapes
        ############################
        self.last_x = 0
        self.last_y = 0
        ############################
        self.enableMovment = False
        self.inPlace = False
        self.Foodseen = [-1]
        self.idx = 0
        ############################
        # PID
        self.mem = 0.0
        self.errorMem = 0.0
        self.P = 0
        self.I = 0
        self.D = 0
        self.avg_error = 0
        ############################

    removed = 0
    infraredRadius = 70
    radius = 0
    foodID_last = []
    kilobotID_last = []
    front_y_conf_val = 2
    moves = 0
    last_closestfood = 0



    def alterSpinCounter(self, value):
        self.spinCounter = self.spinCounter + value
        if self.spinCounter < 50:
            self.spinCounter = 50
        elif self.spinCounter > 100:
            self.spinCounter = 100

    def GetX(self):
        return self.x

    def GetY(self):
        return self.y

    def StoreMotorsValue(self, M1, M2):
        self.M1Motor_val = M1
        self.M2Motor_val = M2

    def GetMotorsValue(self):
        return self.M1Motor_val, self.M2Motor_val

    def SetNewMotorsValue(self, M1, M2):
        self.M1Motor_val = M1
        self.M2Motor_val = M2

    def drawKilobot(self, screen):
        """
            Draws Kilobot on screen
            :param: self
            :param: screen: Window dimensions [x,y]
            :return: none
        """
        pygame.draw.circle(screen, (self.r, self.g, self.b), (int(self.x), int(self.y)), self.radius)
        pygame.draw.circle(screen, (self.front_r, self.front_g, self.front_b), (int(self.front_x), int(self.front_y)),
                           self.front_radius)


    def drawFood(self, screen):
        """
            Draws food on screen
            :param: self
            :param: screen: Window dimensions [x,y]
            :return: none
        """
        pygame.draw.circle(screen, (self.r, self.g, self.b), (int(self.x), int(self.y)), self.radius)

    def setPositon(self, x, y):
        self.x = x
        self.y = y

        self.front_x = x
        self.front_y = y + self.front_y_conf_val

    def changeColor(self, r, g, b):
        """
            Changes color of Kilobot
            :param: self
            :param: r,g,b: RGB values [0-255]
            :return: none
        """
        self.r = r
        self.g = g
        self.b = b

    def changeColorKilobot(self, r, g, b):
        self.r = (255 / 7) * r
        self.g = (255 / 7) * g
        self.b = (255 / 7) * b



    def rotateKilobot(self, spinAngle):
        self.fi = self.fi + spinAngle

    def createStticBody(self):
        self.body.position = (self.x, self.y)

    def MotorsMoveKilobot_learn(self, M1, M2, V):
        """
            Moves Kilobots used for learning
            :param: self
            :param: M1, M2: Activation values for both motors
            :param: v: Parameter used for scaling movement length
            :return: none
        """
        self.V = V
        M_temp = M1 - M2
        self.fi = self.fi + M_temp * 0.01
        xSpeed = sin(radians(self.fi))
        ySpeed = cos(radians(self.fi))
        self.x = self.x + xSpeed * self.V
        self.y = self.y + ySpeed * self.V

        if M_temp != 0:
            self.front_x = self.x + xSpeed * 13
            self.front_y = self.y + ySpeed * 13
        else:
            self.front_x = self.front_x + xSpeed * V
            self.front_y = self.front_y + ySpeed * V

    def MotorsMoveKilobot(self, M1, M2, v):
        """
            Moves Kilobots
            :param: self
            :param: M1, M2: Activation values for both motors
            :param: v: Parameter used for scaling movement length
            :return: none
        """
        M_temp = M1 - M2
        speedMod = (M1+M2)/510
        self.fi = self.fi + M_temp * 0.020
        xSpeed = 100 * sin(radians(self.fi))*v * speedMod
        ySpeed = 100 * cos(radians(self.fi))*v * speedMod
        self.body.angular_velocity = M_temp
        self.body.velocity = (xSpeed, ySpeed)

        self.front_x = self.x + 0.2 * xSpeed
        self.front_y = self.y + 0.2 * ySpeed

    def MotorsMoveKilobot_older(self, M1, M2, v):
        """
                  Moves Kilobots odler version that is usable in creating shapes algorithm
                  :param: self
                  :param: M1, M2: Activation values for both motors
                  :param: v: Parameter used for scaling movement length
                  :return: none
              """
        M_temp = M1 - M2

        self.fi = self.fi + M_temp * 0.01
        xSpeed = 55 * sin(radians(self.fi)) * v
        ySpeed = 55 * cos(radians(self.fi)) * v
        self.body.angular_velocity = M_temp
        self.body.velocity = (xSpeed, ySpeed)

        self.front_x = self.x + 0.5 * xSpeed
        self.front_y = self.y + 0.5 * ySpeed


    def refreshCoord(self):
        """
            Refreshes Kilobots x-y coordinates
            :param: self
            :return: none
        """
        self.x = self.body.position[0]
        self.y = self.body.position[1]

    def simple_move(self, x, y):

        self.x = self.x + x
        self.y = self.y + y

        self.front_x = self.front_x + x
        self.front_y = self.front_y + y

    def calculateSpeedXY(self, speed):
        angle = self.fi * pi / 180
        xSpeed = sin(angle) * speed
        ySpeed = cos(angle) * speed
        return xSpeed, ySpeed


    def isIdPresent(self, inID):
        for itr in self.inIRRangeKilobotID:
            if itr == inID:
                return True
        else:
            return False

    def isFoodIdPresent(self, inID):
        for itr in self.inIRRangeFoodID:
            if itr == inID:
                return True
        else:
            return False

    def detectKilobotsInIRRange(self, kilobotArray):
        """
            Detects Kilobots in IR range
            :param: self
            :param: kilobotArray: Array containing all created Kilobots
            :return: none
        """
        for botItr in kilobotArray:
            xDif = fabs(self.front_x - botItr.x)
            yDif = fabs(self.front_y - botItr.y)
            Dif = sqrt(xDif ** 2 + yDif ** 2)
            if botItr.id == self.id:
                continue
            elif Dif.real < 2 * self.infraredRadius:
                if not botItr.isFoodIdPresent(botItr.id):
                    IDandDistance = [botItr.id, round(Dif.real, 2)]
                    self.inIRRangeKilobotID.append(IDandDistance)

    def detectFoodsInIRRange(self, FoodsArray):
        """
            Detects foods in IR range
            :param: self
            :param: FoodsArray: Array containing all created Foods
            :return: none
        """
        for foodItr in FoodsArray:
            xDif = fabs(self.x - foodItr.x)
            yDif = fabs(self.y - foodItr.y)
            Dif = sqrt(xDif ** 2 + yDif ** 2)
            if Dif.real < 2 * self.infraredRadius:
                if not foodItr.isFoodIdPresent(foodItr.id):
                    IDandDistance = [foodItr.id, round(Dif.real, 2)]
                    self.inIRRangeFoodID.append(IDandDistance)


    def findClosestFood(self):
        """
            Finds closest food
            :param: self
            :return: ID of closest food in range
        """
        if len(self.foodID_last) != 0:
            closest = self.foodID_last[0][1]
            closest_id = 0

            for food in range(0, len(self.foodID_last)):
                if self.foodID_last[food][1] < closest:
                    closest = self.foodID_last[food][1]
                    closest_id = food
            return closest_id
        else:
            return None

    def findClosestKilobot(self):
        """
            Finds closest kilobot
            :param: self
            :return: ID of closest food in range
        """
        if len(self.inIRRangeKilobotID) != 0:
            closest = self.inIRRangeKilobotID[0][1]
            closest_id = 0

            for kilobot in range(0, len(self.inIRRangeKilobotID)):
                if self.inIRRangeKilobotID[kilobot][1] < closest:
                    closest = self.inIRRangeKilobotID[kilobot][1]
                    closest_id = kilobot
            return closest_id
        else:
            return None

    def checkIfNewTargetWasAcquired(self, previousTargetID):
        if previousTargetID is not self.targetBotID and self.targetBotID is not self.id:
            self.newTarget = self.newTarget + 1
            self.spinCounter = 100
            self.detectOscilations = 0
        if previousTargetID is not self.targetBotID and self.targetBotID is self.id:
            self.lostTarget = self.lostTarget + 1

    def findLowerIDBot(self):
        self.targetBotID = self.id
        for botID1 in self.inIRRangeKilobotID:
            x = int(botID1[0])
            y = int(self.id)
            if x < y:
                self.targetBotID = botID1[0]
        self.checkIfNewTargetWasAcquired(self.previousTarget)
        print(str(self.id) + "now follows" + str(self.targetBotID))
        print(self.newTarget)
        self.previousTarget = self.targetBotID

    def calcPID(self, input, measurement, KP, KI, KD, Upperlimit, Lowerlimit, Sampletime):
        """
           calculate`s output of PID regulator
           :param: self
           :param input: reference value
           :param measurement: value to create feedback loop
           :param KP: KP setting
           :param KI: KI setting
           :param KD: KD setting
           :param Upperlimit: upper limit that output can`t cross
           :param Lowerlimit: lower limit that output can`t cross
           :param Sampletime: time step
           :return: control output
           """
        # calculating error
        error = (input - measurement)

        # calculating P,I,D outputs
        outP = error * KP
        outI = error * KI * Sampletime + self.mem
        outD = ((error - self.errorMem) / Sampletime) * KD

        # anti windup
        if outI > 255 or outI < 0:
            outI = self.mem

        # checking I output boundaries
        if outI > Upperlimit:
            outI = Upperlimit
        if outI < Lowerlimit:
            outI = Lowerlimit

        # calculating global output
        out = outP + outI + outD

        # checking output boundaries
        if out > Upperlimit:
            out = Upperlimit
        if out < Lowerlimit:
            out = Lowerlimit

        # saving data
        self.mem = outI
        self.errorMem = error

        return out

    def calcPD(self,  input, measurement, KP, KD, Upperlimit, Lowerlimit,Sampletime):
        """
            calculate`s output of PID regulator
            :param: self
            :param input: reference value
            :param measurement: value to create feedback loop
            :param KP: KP setting
            :param KD: KD setting
            :param Upperlimit: upper limit that output can`t cross
            :param Lowerlimit: lower limit that output can`t cross
            :param Sampletime: time step
            :return: control output
        """

        # calculating error
        error = (input - measurement)

        # calculating P,I,D outputs
        outP = error * KP
        outD = ((error - self.errorMem) / Sampletime) * KD

        # calculating global output
        out = outP + outD

        # checking output boundaries
        if out > Upperlimit:
            out = Upperlimit
        if out < Lowerlimit:
            out = Lowerlimit

        # saving data
        self.errorMem = error

        return out

    def calcPI(self, input, measurement, KP, KI, Upperlimit, Lowerlimit, Sampletime):
        """
            calculate`s output of PID regulator
            :param: self
            :param input: reference value
            :param measurement: value to create feedback loop
            :param KP: KP setting
            :param KI: KI setting
            :param Upperlimit: upper limit that output can`t cross
            :param Lowerlimit: lower limit that output can`t cross
            :param Sampletime: time step
            :return: control output
        """
        # calculating error
        error = (input - measurement)

        # calculating P,I,D outputs
        outP = error * KP
        outI = error * KI * Sampletime + self.mem

        # anti windup
        if outI > 255 or outI < 0:
            outI = self.mem

        # checking I output boundaries
        if outI > Upperlimit:
            outI = Upperlimit
        if outI < Lowerlimit:
            outI = Lowerlimit

        # calculating global output
        out = outP + outI

        # checking output boundaries
        if out > Upperlimit:
            out = Upperlimit
        if out < Lowerlimit:
            out = Lowerlimit

        # saving data
        self.mem = outI

        return out


    def setPID(self, P, I, D):
        """
            set PID values
            :param: self
            :param P: value of P
            :param I: value of I
            :param D: value of D
            :return: None
        """

        self.P = P
        self.I = I
        self.D = D

    def getPID(self):
        """
            get PID values
            :param: self
            :return P: value of P
            :return I: value of I
            :return D: value of D
        """
        return self.P, self.I, self.D


    def savePID(self):
        """
            save PID values
            :param: self
            :return None
        """
        f = open("PID_val.txt", "w")
        text = str(round(self.P, 2)) + "," + str(round(self.I, 2)) + "," + str(round(self.D, 2))
        f.write(str(text))
        f.close()


    def loadPID(self, idx):
        """
            loads PID values and randomize them
            :param: self
            :param: idx: index of genome
            :return None
        """
        f = open("PID_val.txt", "r")

        text = f.readline()

        line = text.split(",")

        # convert each element as integers
        values = []
        for i in line:
            values.append(float(i))

        rand = BasicFunc.getRandSpin()

        if idx < 10:
            if idx != 0:
                self.P = values[0] / rand
                rand = BasicFunc.getRandSpin()
                self.I = values[1] / rand
                rand = BasicFunc.getRandSpin()
                self.D = values[2] / rand
                rand = BasicFunc.getRandSpin()
            else:
                self.P = values[0]
                self.I = values[1]
                self.D = values[2]
        if 10 <= idx < 20:
            self.P = values[0] + rand
            rand = BasicFunc.getRandSpin()
            self.I = values[1] + rand
            rand = BasicFunc.getRandSpin()
            self.D = values[2] + rand
            rand = BasicFunc.getRandSpin()
        if 20 <= idx <= 30:
            self.P = values[0] - rand
            rand = BasicFunc.getRandSpin()
            self.I = values[1] - rand
            rand = BasicFunc.getRandSpin()
            self.D = values[2] - rand

        if self.P <= 0:
            self.P = 0.1
        if self.I <= 0:
            self.I = 0.1
        if self.D <= 0:
            self.D = 0.1