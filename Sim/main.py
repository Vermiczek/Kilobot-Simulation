import pygame
import os
import AI_sim_verion
import CreatingShapesAlgorithm
import FoodFinding
import numpy as np
import matplotlib.pyplot as plt

# inicjalizacja biblioteki
pygame.init()

#press 0 for fuzzy movement (doesn't work), 1 for food search, 2 for line movement
#place kilobots with left mouse button, place food with space button
FoodFinding.Control()

#####################################################################################################
# creating shapes algorithm
# error_output = CreatingShapesAlgorithm.PIDcontrol()
#
# x_error_dist = np.arange(0, len(error_output[1]), 1)
# wart_zadana = np.full([len(error_output[1])], 35)
#
# # neural regulator plot
# # plt.plot(x_error_dist, error_output[0], 'b-', label='uchyb')
# plt.plot(x_error_dist, error_output[1], 'g-', label='odległość od najbliższego kilobota')
# plt.plot(x_error_dist, wart_zadana, 'r-', label='wartość zadana')
# plt.xlabel('numer próbki', fontsize=18)
# # plt.ylabel('uchyb regulacji [1.1mm]', fontsize=16)
# plt.ylabel('odległość od najbliższego kilobota [1.1mm]', fontsize=16)
# plt.legend(prop={'size': 20})
# plt.grid()
# plt.show()

#####################################################################################################
# NEURAL regulator algorithm
if __name__ == '__main__':
    # Determine path to configuration file. This path manipulation is
    # here so that the script will run successfully regardless of the
    # current working directory
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config_neat.txt')
    error_output = AI_sim_verion.run_results(config_path)
    print("done")
    x_error_dist = np.arange(0, len(error_output[1]), 1)
    wart_zadana = np.full([len(error_output[1])], 35)

    # neural regulator plot
    # plt.plot(x_error_dist, error_output[0], 'b-', label='uchyb')
    plt.plot(x_error_dist, error_output[1], 'g-', label='odległość od najbliższego kilobota')
    plt.plot(x_error_dist, wart_zadana, 'r-', label='wartość zadana')
    plt.xlabel('numer próbki', fontsize=18)
    # plt.ylabel('uchyb regulacji [1.1mm]', fontsize=16)
    plt.ylabel('odległość od najbliższego kilobota [1.1mm]', fontsize=16)
    plt.legend(prop={'size': 20})
    plt.grid()
    plt.show()

######################################################################################################
# NEURAL regulator learning
# if __name__ == '__main__':
#     # Determine path to configuration file. This path manipulation is
#     # here so that the script will run successfully regardless of the
#     # current working directory
#     local_dir = os.path.dirname(__file__)
#     config_path = os.path.join(local_dir, 'config_neat.txt')
#     AI_sim_verion.run(config_path)


######################################################################################################
