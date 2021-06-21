import pygame
from button import button
from timer import Timer
import neat
import Movement
import kilobotClass
import BasicFunc
import pymunk
import invisibleWall
import Shapes

resx = 1200
resy = 800

screen = pygame.display.set_mode((resx, resy))


def PIDcontrol():
    """
        PID, PD, PI movement version of simulation
        :return: None
        or
        :return: error_output: list of two lists containing data about movement(error and distance)
    """
    global FoodID, kilobotID, kilobotsNumber, FoodNumber
    # creating config data
    kilobotsMaxAmount = 100
    kilobots = []
    Foods = []
    kilobots.clear()
    kilobotID = 0
    kilobotsNumber = 0
    FoodID, FoodNumber = 0, 0
    startTime = 0
    enable = False
    wallsBuilt = 0
    Ts = 1
    error = 0
    distnace = 35
    shape_itr = 0
    lest_kilobots_in_range = 10000
    error_output = [[],[]]
    currentAlghoritm = 0

    # creating buttons
    resetButton = button((220, 220, 220), resx - 100, resy - 50, 100, 50, 'Reset', True)
    startButton = button((220, 220, 220), 0, resy - 50, 100, 50, 'Start', True)
    pauseButton = button((220, 220, 220), resx / 2 - 50, resy - 50, 100, 50, 'Pause', True)
    numberView = button((255, 255, 255), resx / 2 - 50, 50, 100, 50, str(kilobotsNumber), False)
    timeView = button((255, 255, 255), resx - 50, 0, 50, 50, str(startTime), False)

    # timers and loop config
    running = True
    t = Timer()
    t_pause = Timer()
    t.set_default()
    t_pause.set_default()

    # creating physics space
    space = pymunk.Space()
    # creating fps clock
    clock = pygame.time.Clock()

    x = 100
    y = 300

    # create population of objects
    # comment to disable auto placement
    for i in range(0, 20):
        position = [x, y]
        kilobots, kilobotID, kilobotNumber, space = BasicFunc.addKilobotEventAI(position, kilobots, kilobotID,
                                                                                kilobotsNumber, space)
        x = x + 35

    # add object to create from kilobots
    shape = BasicFunc.addShapeEvent([800, 300], 100)

    # main loop
    while running:
        clock.tick(400)
        screen.fill((255, 255, 255))

        # building walls
        if wallsBuilt == 0:
            space = BasicFunc.buildWalls(screen, resx, resy, space)
            wallsBuilt = 1

        # mouse input handler
        t, enable, t_pause, kilobots, Foods, kilobotID, kilobotsNumber, FoodID, FoodNumber, space, currentAlghoritm, wallsBuilt = BasicFunc.inputEventHandler(
                t, enable, t_pause, kilobots, Foods, kilobotID, kilobotsNumber, FoodID, FoodNumber, startButton,
                pauseButton, resetButton, space, currentAlghoritm, wallsBuilt)

        # update list of food in range
        for itr in kilobots:
            itr.inIRRangeKilobotID.clear()
            itr.inIRRangeFoodID.clear()
            itr.refreshCoord()

        # set 0 velocity for static kilobots
        for itr in Foods:
            itr.body.velocity = (0, 0)
            itr.refreshCoord()

        # set 0 velocity for kilobots that are not enable to move
        for x, itr in enumerate(kilobots):
            if x == shape_itr:
                continue
            else:
                itr.body.velocity = (0, 0)
                itr.refreshCoord()

        # detect kilobots in range and static kilobots in range that are not enabled to move
        BasicFunc.detectFoodsInIRRange(kilobots, Foods)
        BasicFunc.detectKilobotsInIRRange(kilobots)

        # creatng shape action
        if len(kilobots) > 0 and shape_itr < len(kilobots):

            # check if Klobot is in place and movement is enabled
            if kilobots[shape_itr].inPlace == False and enable == True:

                # enable motors movement
                kilobots[shape_itr].enableMovment = True

                # pid movement of kilobots
                val1, val2 = Movement.kilobotPIDmovement(enable, kilobots[shape_itr], screen, Ts, distnace)

                # add data to output vector
                # error
                error_output[0].append(val1)
                # distance
                error_output[1].append(val2)

                # check if kilobot is in place
                if shape.IsKilobotInsigt(kilobots[shape_itr]):
                    # if kilobot is in place switch off motors and disable movement
                    kilobots[shape_itr].inPlace = True
                    kilobots[shape_itr].enableMovment = False
                    shape_itr += 1

########################################################################################################################
                    # uncomment ro return output
                    return error_output
########################################################################################################################

        # create last seen kilobots vector
        BasicFunc.FoodsInIRRange_last(kilobots)
        BasicFunc.KilobotsInIRRange_last(kilobots)

        # drawing objets
        shape.drawCircle(screen)
        kilobotClass.drawKilobots(kilobots, screen)
        kilobotClass.drawKilobots(Foods, screen)

        # update physics engine
        space.step(1 / 50)

        # setting number of kilobots in simulation
        numberView.text = str(kilobotsNumber)
        timeView.text = str(t.read_time())

        # drawing other objects
        BasicFunc.drawWalls(screen, resx, resy)
        resetButton.draw(screen)
        startButton.draw(screen)
        pauseButton.draw(screen)
        numberView.draw(screen)
        timeView.draw(screen)

        pygame.display.update()


###########################################################################3
def NEURALcontrol(genomes, config):
    """
        Neural movement version of simulation
        :param genomes: list that contains objects with NNs
        :param config: config data of NNs
        :return: None
        or
        :return: error_output: list of two lists containing data about movement(error and distance)
    """
    global FoodID, kilobotID, kilobotsNumber, FoodNumber
    # creating config data
    Foods = []
    kilobotID = 0
    kilobotsNumber = 0
    FoodID, FoodNumber = 0, 0
    startTime = 0
    enable = False
    wallsBuilt = 0
    Ts = 1
    distnace = 35
    shape_itr = 0
    error_output = [[], []]
    currentAlghoritm = 0

    # creating buttons
    resetButton = button((220, 220, 220), resx - 100, resy - 50, 100, 50, 'Reset', True)
    startButton = button((220, 220, 220), 0, resy - 50, 100, 50, 'Start', True)
    pauseButton = button((220, 220, 220), resx / 2 - 50, resy - 50, 100, 50, 'Pause', True)
    numberView = button((255, 255, 255), resx / 2 - 50, 50, 100, 50, str(kilobotsNumber), False)
    timeView = button((255, 255, 255), resx - 50, 0, 50, 50, str(startTime), False)

    # timers and loop config
    running = True
    t = Timer()
    t_pause = Timer()
    t.set_default()
    t_pause.set_default()

    # creating physics space
    space = pymunk.Space()
    # creating fps clock
    clock = pygame.time.Clock()

    # start by creating lists holding the genome itself, the
    # neural network associated with the genome and the
    # kilobot object that uses that network to learn
    nets = []
    kilobots = []
    kilobots.clear()
    ge = []

    x = 100
    y = 300

    # create population of objects
    for genome_id, genome in genomes:
        genome.fitness = 0  # start with fitness level of 0
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        nets.append(net)

        position = [x, y]
        kilobots, kilobotID, kilobotNumber, space = BasicFunc.addKilobotEventAI(position, kilobots, kilobotID,
                                                                                kilobotsNumber, space)
        ge.append(genome)
        x = x + 35

    # add object to create from kilobots
    shape = BasicFunc.addShapeEvent([800, 300], 100)

    # main loop
    while running:
        time = t.read_time()
        clock.tick(400)
        screen.fill((255, 255, 255))

        # building walls
        if wallsBuilt == 0:
            space = BasicFunc.buildWalls(screen, resx, resy, space)
            wallsBuilt = 1


        # mouse input handler
        t, enable, t_pause, kilobots, Foods, kilobotID, kilobotsNumber, FoodID, FoodNumber, space, currentAlghoritm, wallsBuilt = BasicFunc.inputEventHandler(
            t, enable, t_pause, kilobots, Foods, kilobotID, kilobotsNumber, FoodID, FoodNumber, startButton,
            pauseButton, resetButton, space, currentAlghoritm, wallsBuilt)

        # update list of food in range
        for itr in kilobots:
            itr.inIRRangeKilobotID.clear()
            itr.inIRRangeFoodID.clear()
            itr.refreshCoord()

        # set 0 velocity for static kilobots
        for itr in Foods:
            itr.body.velocity = (0, 0)
            itr.refreshCoord()

        # set 0 velocity for kilobots that are not enable to move
        for x, itr in enumerate(kilobots):
            if x == shape_itr:
                continue
            else:
                itr.body.velocity = (0, 0)
                itr.refreshCoord()

        # detect kilobots in range and static kilobots in range that are not enabled to move
        BasicFunc.detectFoodsInIRRange(kilobots, Foods)
        BasicFunc.detectKilobotsInIRRange(kilobots)

        # creatng shape action
        # check if kilobots array exist
        if len(kilobots) > 0 and shape_itr < len(kilobots):

            # check if Klobot is in pace and movement is enabled
            if kilobots[shape_itr].inPlace == False and enable == True:

                # enable motors movement
                kilobots[shape_itr].enableMovment = True

                # find closest kilobot
                closestKilobot = kilobots[shape_itr].findClosestKilobot()
                if closestKilobot is None:
                    closestKilobot = 0

                # calculating  current error
                fitness = distnace - kilobots[shape_itr].inIRRangeKilobotID[closestKilobot][1]

                # calculate net`s output
                output = nets[shape_itr].activate([fitness, kilobots[shape_itr].inIRRangeKilobotID[closestKilobot][1]])

                # choose output with highest activation
                max_value = max(output)
                max_index = output.index(max_value)

                # perform actions
                if max_index == 0 and output[0] > 0.5:
                    output_val = 0
                if max_index == 1 and output[1] > 0.5:
                    output_val = 1
                if max_index == 2 and output[2] > 0.5:
                    output_val = -1

                # for i in range(0, 127):
                #     if max_index == i and output[i] > 0.5:
                #         output_val = i

                # neural reg movment of kilobots
                Movement.kilobotNeuralmovement(enable, kilobots[shape_itr], screen, output_val)

                # add data to output vector
                # error
                error_output[0].append(fitness)
                # distance
                error_output[1].append(kilobots[shape_itr].inIRRangeKilobotID[closestKilobot][1])

                # check if kilobot is insight light source and set flags if true
                if shape.IsKilobotInsigt(kilobots[shape_itr]):
                    kilobots[shape_itr].inPlace = True
                    kilobots[shape_itr].enableMovment = False
                    shape_itr += 1
########################################################################################################################
                    # uncomment ro return output
                    return error_output
########################################################################################################################

        # create last seen kilobots vector
        BasicFunc.FoodsInIRRange_last(kilobots)
        BasicFunc.KilobotsInIRRange_last(kilobots)

        # drawing objets
        shape.drawCircle(screen)
        kilobotClass.drawKilobots(kilobots, screen)
        kilobotClass.drawKilobots(Foods, screen)

        # update physics engine
        space.step(1 / 50)

        # setting number of kilobots in simulation
        numberView.text = str(kilobotsNumber)
        timeView.text = str(t.read_time())

        # drawing other objects
        BasicFunc.drawWalls(screen, resx, resy)
        resetButton.draw(screen)
        startButton.draw(screen)
        pauseButton.draw(screen)
        numberView.draw(screen)
        timeView.draw(screen)

        pygame.display.update()
