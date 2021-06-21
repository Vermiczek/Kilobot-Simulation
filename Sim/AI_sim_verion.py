import pygame
from button import button
from timer import Timer
import neat
import Movement
import kilobotClass
import BasicFunc
import pickle
import gzip
import pymunk
import CreatingShapesAlgorithm
import visualize


resx = 1200
resy = 800



def run(config_file):
    """
    runs the NEAT algorithm to train a neural network.
    :param config_file: location of config file
    :return: None
    """
    global gen
    gen = BasicFunc.GetGenerationNumber()

    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                                neat.DefaultSpeciesSet, neat.DefaultStagnation,
                                config_file)

    # Create the population, which is the top-level object for a NEAT run.
    p = neat.Population(config)
    # Create the population from checkpoint
    #p = neat.Checkpointer.restore_checkpoint('neat-checkpoint-912')

    # Add a stdout reporter to show progress in the terminal.
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    # collect data to save
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    # set number of data to save
    p.add_reporter(neat.Checkpointer(1, None))


    # Run for up to x generations.
    winner = p.run(ai_neural_regulator, 1)

    # visualisation(doesn`t work)
    # visualize.draw_net(config, winner, True)
    # visualize.plot_stats(stats, ylog=False, view=True)
    # visualize.plot_species(stats, view=True)

    # save data to file
    stats.save()
    # save generation number
    BasicFunc.SaveGenerationNumber(gen)

    # show final stats
    print('\nBest genome:\n{!s}'.format(winner))

    p.remove_reporter(stats)

    # save results
    with open("network.pkl", "wb") as f:
        pickle.dump(winner, f)
        f.close()


def run_results(config_file, genome_path="regulator_neuronowy.pkl"):
    """
       runs the NEAT algorithm to train a neural network.
       :param config_file: location of config file
       :return: error_output: return vector of two vectors which
    """
    # Load requried NEAT config
    global gen
    gen = BasicFunc.GetGenerationNumber()

    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet,
                                neat.DefaultStagnation, config_file)

    genomes = []
    # Unpickle saved winner
    with open(genome_path, "rb") as f:
        genome = pickle.load(f)

    # Convert loaded genome into required data structure
    for i in range(1, 20):
        genome_t = (i, genome)
        genomes.append(genome_t)

    # Call game with only the loaded genome
    error_output = CreatingShapesAlgorithm.NEURALcontrol(genomes, config)
    return error_output




########################################################################################################################
def ai_shape_test(genomes, config):
    """
            runs the NEAT algorithm to train PID tuner:
            :param genomes: object that contains information about genomes(neural networks)
            :param config: config of neural networks
            :return: None
            """

    global gen
    gen += 1
    # create Pygame object
    screen = pygame.display.set_mode((resx, resy))

    global FoodID, kilobotID, kilobotsNumber, FoodNumber
    # creating config data
    Foods = []
    kilobotID = 0
    kilobotsNumber = 0
    FoodID, FoodNumber = 0, 0
    startTime = 0
    error_itr = 0
    Ts = 1/400
    distnace = 50
    min_error = 1000

    # create buttons
    resetButton = button((220, 220, 220), resx - 100, resy - 50, 100, 50, 'Reset', True)
    startButton = button((220, 220, 220), 0, resy - 50, 100, 50, 'Start', True)
    pauseButton = button((220, 220, 220), resx / 2 - 50, resy - 50, 100, 50, 'Pause', True)
    numberView = button((255, 255, 255), resx / 2 - 50, 50, 100, 50, str(gen), False)
    timeView = button((255, 255, 255), resx - 50, 0, 50, 50, str(startTime), False)

    # timers and loop config
    running = True
    t = Timer()
    t_pause = Timer()
    t.set_default()
    t_pause.set_default()
    clock = pygame.time.Clock()

    # creating physics space
    space = pymunk.Space()

    # start by creating lists holding the genome itself, the
    # neural network associated with the genome and the
    # kilobot object that uses that network to learn
    nets = []
    kilobots = []
    kilobots.clear()
    ge = []

    idx = 0
    x = 550
    y = 400

    # create population of objects to learn
    for genome_id, genome in genomes:
        genome.fitness = 0  # start with fitness level of 0
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        nets.append(net)


        # create kilobots that are able to move
        position = [x, y]
        kilobots, kilobotID, kilobotNumber, space = BasicFunc.addKilobotEventAI(position, kilobots, kilobotID,
                                                                                kilobotsNumber, space)
        ge.append(genome)
        # x = x + 1000

        kilobots[idx].loadPID(idx * 1)
        idx += 1

    x = 600
    y = 400

    # creating group of kilobots
    for i_y in range(0, 4):
        FoodID += 1

        position2 = [x, y]
        Foods, space = (BasicFunc.addFoodEventAI(position2, Foods, FoodID, 0, 128, 0, space))

        FoodID += 1
        position2 = [x, y + 35]
        Foods, space = (BasicFunc.addFoodEventAI(position2, Foods, FoodID, 0, 128, 0, space))

        x = x + 35

    # start timer and simulation manually
    t, enable, t_pause = BasicFunc.startEventmanual(t, t_pause)

    # start main loop
    while running and len(kilobots) > 0:
        # set clock
        clock.tick(400)
        screen.fill((255, 255, 255))


        # update list of food in range
        for itr in kilobots:
            itr.inIRRangeKilobotID.clear()
            itr.inIRRangeFoodID.clear()

        # detect kilobots in range and static kilobots in range that are not enabled to move
        BasicFunc.detectFoodsInIRRange(kilobots, Foods)
        BasicFunc.detectKilobotsInIRRange(kilobots)

        # loop that iterate moving kilobots vector and moves kilobots
        for kilobot in kilobots:
            kilobot.enableMovment = True
            Movement.kilobotPIDmovement_tunning(enable, kilobot, screen, Ts, distnace)


        # read time
        time = t.read_time()

        # increase number that counts iterations
        error_itr = error_itr + 1

        # create vector that contains static kilobots that has been seen in previous iteration
        BasicFunc.FoodsInIRRange_last(kilobots)

        # loop that iterate moving kilobots vector
        for x, kilobot in enumerate(kilobots):

            # find closest food
            closestFood = kilobot.findClosestFood()
            if closestFood is None:
                closestFood = 0


            if kilobot.inIRRangeFoodID[closestFood][1] > 1000:
                ge[x].fitness -= 1000
                nets.pop(x)
                ge.pop(x)
                kilobots.pop(x)
                continue

            # calculating  current error
            fitness = distnace - kilobot.inIRRangeFoodID[closestFood][1]

            # calculating output of Gaussian function
            gausian = BasicFunc.gaussian(fitness, 0.001, 0)

            # adding output of Gaussian function to global fitness
            ge[x].fitness += gausian * 0.000001

            # adding value global fitness
            if gausian == 0:
                ge[x].fitness -= fitness * 0.01

            # calculate sum of errors
            kilobot.avg_error = kilobot.avg_error + abs(distnace - kilobot.inIRRangeFoodID[closestFood][1])

            # update last seen closest kilobot
            kilobot.last_closestfood = closestFood

            if error_itr > 800:

                # get PID value
                P, I, D = kilobot.getPID()

                # calculate average error
                avg_error = kilobot.avg_error / error_itr

                # check if this kilobot if the best to save
                if avg_error < min_error:

                    # calculate net`s output
                    output = nets[x].activate([avg_error])

                    # perform actions
                    if output[0] > 0.5:
                        P = P + 0.1
                    if output[1] > 0.5:
                        P = P + 0.01
                    if output[2] > 0.5:
                        P = P + 0
                    if output[3] > 0.5:
                        P = P - 0.01
                    if output[4] > 0.5:
                        P = P - 0.1
                    if output[5] > 0.5:
                        I = I + 0.1
                    if output[6] > 0.5:
                        I = I + 0.01
                    if output[7] > 0.5:
                        I = I + 0
                    if output[8] > 0.5:
                        I = I - 0.01
                    if output[9] > 0.5:
                        I = I - 0.1
                    if output[10] > 0.5:
                        D = D + 0.1
                    if output[11] > 0.5:
                        D = D + 0.01
                    if output[12] > 0.5:
                        D = D + 0
                    if output[13] > 0.5:
                        D = D - 0.01
                    if output[14] > 0.5:
                        D = D - 0.1

                    # set new PID values
                    kilobot.setPID(P, I, D)

                    # save new PID values
                    kilobot.savePID()

                    # update best kilobot to save
                    min_error = avg_error

                # delate kilobot
                nets.pop(x)
                ge.pop(x)
                kilobots.pop(x)

        # draw objects
        kilobotClass.drawKilobots(kilobots, screen)
        kilobotClass.drawKilobots(Foods, screen)

        # draw data in simulation
        numberView.text = str(kilobotsNumber)
        timeView.text = str(time)
        resetButton.draw(screen)
        startButton.draw(screen)
        pauseButton.draw(screen)
        numberView.draw(screen)
        timeView.draw(screen)

        pygame.display.update()


########################################################################################################################
def ai_neural_regulator(genomes, config):
    """
        runs the NEAT algorithm to train a neural reagulator:
        :param genomes: object that contains information about genomes(neural networks)
        :param config: config of neural networks
        :return: None
        """
    global gen
    gen += 1
    # create Pygame object
    screen = pygame.display.set_mode((resx, resy))

    global FoodID, kilobotID, kilobotsNumber, FoodNumber
    # creating config data
    Foods = []
    kilobotID = 0
    kilobotsNumber = 0
    FoodID, FoodNumber = 0, 0
    startTime = 0
    error_itr = 0
    distnace = 35
    output_val = 0

    # create buttons
    resetButton = button((220, 220, 220), resx - 100, resy - 50, 100, 50, 'Reset', True)
    startButton = button((220, 220, 220), 0, resy - 50, 100, 50, 'Start', True)
    pauseButton = button((220, 220, 220), resx / 2 - 50, resy - 50, 100, 50, 'Pause', True)
    numberView = button((255, 255, 255), resx / 2 - 50, 50, 100, 50, str(gen), False)
    timeView = button((255, 255, 255), resx - 50, 0, 50, 50, str(startTime), False)

    # timers and loop config
    running = True
    t = Timer()
    t_pause = Timer()
    t.set_default()
    t_pause.set_default()
    clock = pygame.time.Clock()

    # creating physics space
    space = pymunk.Space()

    # start by creating lists holding the genome itself, the
    # neural network associated with the genome and the
    # kilobot object that uses that network to learn
    nets = []
    kilobots = []
    kilobots.clear()
    ge = []


    x = 100
    y = 300

    # create population of objects to learn
    for genome_id, genome in genomes:
        genome.fitness = 0  # start with fitness level of 0
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        nets.append(net)

        # create kilobots that are able to move
        position = [x, y]
        kilobots, kilobotID, kilobotNumber, space = BasicFunc.addKilobotEventAI(position, kilobots, kilobotID,
                                                                                kilobotsNumber, space)
        ge.append(genome)


    x = 135
    y = 300
    # creating group of kilobots
    for i_y in range(0, 19):
        FoodID += 1

        position2 = [x, y]
        Foods, space = (BasicFunc.addFoodEventAI(position2, Foods, FoodID, 0, 128, 0, space))
        x = x + 35

    # start timer and simulation manually
    t, enable, t_pause = BasicFunc.startEventmanual(t, t_pause)

    # start main loop
    while running and len(kilobots) > 0:
        # set clock
        clock.tick(400)
        screen.fill((255, 255, 255))

        # update list of food in range
        for itr in kilobots:
            itr.inIRRangeKilobotID.clear()
            itr.inIRRangeFoodID.clear()

        # detect kilobots in range and static kilobots in range that are not enabled to move
        BasicFunc.detectFoodsInIRRange(kilobots, Foods)
        BasicFunc.detectKilobotsInIRRange(kilobots)

        #read time
        time = t.read_time()

        # increase number that counts iterations
        error_itr = error_itr + 1

        # create vector that contains static kilobots that has been seen in previous iteration
        BasicFunc.FoodsInIRRange_last(kilobots)


        # loop that iterate moving kilobots vector
        for x, kilobot in enumerate(kilobots):

            # find closest food
            closestFood = kilobot.findClosestFood()
            if closestFood is None:
                closestFood = 0

            # boundaries to prevent kiloots moving away from group
            if kilobot.inIRRangeFoodID[closestFood][1] > 100:
                ge[x].fitness -= 50
                nets.pop(x)
                ge.pop(x)
                kilobots.pop(x)
                continue

            if kilobot.inIRRangeFoodID[closestFood][1] < 20:
                ge[x].fitness -= 5
                nets.pop(x)
                ge.pop(x)
                kilobots.pop(x)
                continue

            # calculating  current error
            fitness = distnace - kilobot.inIRRangeFoodID[closestFood][1]

            # calculating output of Gaussian function
            gausian = BasicFunc.gaussian(fitness, 0.001, 0)

            # adding output of Gaussian function to global fitness
            ge[x].fitness += gausian * 0.000001

            # adding scalable value to global fitness if output of gaussian is 0
            if gausian == 0:
                ge[x].fitness -= fitness * 0.01


            # calculate sum of errors
            kilobot.avg_error = kilobot.avg_error + abs(distnace - kilobot.inIRRangeFoodID[closestFood][1])

            # calculate net`s output
            output = nets[x].activate([fitness, kilobot.inIRRangeFoodID[closestFood][1]])

            # update vector of seen food
            if kilobot.Foodseen[kilobot.idx] != closestFood:
                kilobot.Foodseen.append(closestFood)
                kilobot.idx += 1

            # find biggest neural network output
            max_value = max(output)
            max_index = output.index(max_value)

            # perform actions for 127 outputs
            # for i in range(0, 127):
            #     if max_index == i and output[i] > 0.5:
            #         output_val = i

            # perform actions for 3 outputs
            if max_index==0 and output[0] > 0.5:
                output_val = 0
            if max_index==1 and output[1] > 0.5:
                output_val = 1
            if max_index==2 and output[2] > 0.5:
                output_val = -1
            if max_index==3 and output[3] > 0.5:
                output_val = 0.5
            if max_index==4 and output[4] > 0.5:
                output_val = -0.5
            # pass control value to motors control function
            Movement.kilobotNeuralmovement_learning(enable, kilobot, screen, output_val)

            # update last seen closest kilobot
            kilobot.last_closestfood = closestFood

            # if iteration of loop id bigger than 7000 end this simulation and save data
            if error_itr > 7000:

                # check seen food vector and give additional fitness points
                # this prevents neural contorler from only rotating kilobots
                for i in kilobot.Foodseen:
                    # if i==7 or i==8 or i==6 or i==16:
                    if i == 19:
                        flag = 1
                        break
                    else:
                        flag = 0
                if flag == 0:
                    ge[x].fitness -= 10000
                flag = 0

                nets.pop(x)
                ge.pop(x)
                kilobots.pop(x)

        # draw objects
        kilobotClass.drawKilobots(kilobots, screen)
        kilobotClass.drawKilobots(Foods, screen)

        # draw data in simulation
        numberView.text = str(kilobotsNumber)
        timeView.text = str(time)
        resetButton.draw(screen)
        startButton.draw(screen)
        pauseButton.draw(screen)
        numberView.draw(screen)
        timeView.draw(screen)

        pygame.display.update()
