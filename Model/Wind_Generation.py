# Purpose: Generate Wind Map
#
#   Info: Class to Weather map that can be
#
#   Developed as part of the Software Agents Course at City University
#
#   Dev: Dan Dixey and Enrico Lopedoto
#
#
import numpy as np
from random import randint, random, sample
import logging


# Logging Controls Level of Printing
logging.basicConfig(format='[%(asctime)s] : [%(levelname)s] : [%(message)s]',
                    level=logging.INFO)


class Obstacle_Tracks(object):

    def __init__(self, WINDOW_HEIGHT, WINDOW_WIDTH,
                 MAX_OBS_HEIGHT, MAX_OBS_WIDTH, N_OBSTABLE_GEN,
                 MIN_GAP, N_TRACKS_GEN):
        # set design parameters:
        self.WINDOW_HEIGHT = WINDOW_HEIGHT
        self.WINDOW_WIDTH = WINDOW_WIDTH
        self.MAX_OBS_HEIGHT = MAX_OBS_HEIGHT
        self.MAX_OBS_WIDTH = MAX_OBS_WIDTH
        self.N_OBSTABLE_GEN = N_OBSTABLE_GEN
        self.MIN_GAP = MIN_GAP
        self.N_TRACKS_GEN = N_TRACKS_GEN
        self.n = self.WINDOW_HEIGHT * self.WINDOW_WIDTH

    def user_function(self, x, y):
        # return (1-x/2+x**5+y**3)*np.exp(-x**2-y**2)
        return x**2 + 2 * y**2
        # return (1-(x+y**3))*np.exp(-(x**2+y**2)/2)

    def generate_obstacles(self):

        obstacles = self.get_obstable_metrics()

        obstacle_arrays = []

        for nb_obstacle in obstacles:

            empty_array = np.zeros(shape=(self.WINDOW_HEIGHT,
                                          self.WINDOW_WIDTH))

            start_location = 0 if nb_obstacle[2] == 1 else self.WINDOW_HEIGHT
            y, x = start_location - 1, nb_obstacle[3]

            empty_array[y, x] = -1

            for w_value in range(nb_obstacle[0]):

                x_updated = x + w_value

                for h_value in range(nb_obstacle[1]):

                    if nb_obstacle[2] == 1:

                        y_updated = y + h_value

                    else:

                        y_updated = y - h_value

                    # Replace Value
                    empty_array[y_updated, x_updated] = -1

            new_array = self.trim_whitespace(empty_array,
                                             nb_obstacle[2],
                                             self.MIN_GAP)

            obstacle_arrays.append(new_array)

        return obstacle_arrays

    def get_obstable_metrics(self):

        obstacle_details = []

        for nb_obstacle in range(self.N_OBSTABLE_GEN):
            # Width Random Size
            width_obs = randint(1, self.MAX_OBS_WIDTH)
            # Height Random Size
            height_obs = randint(1, self.MAX_OBS_HEIGHT)
            # Location Random Selection - 1 if Upper 0 Lower
            location_obs = 1 if random() > 0.5 else 0
            # Start Location
            location_st_obs = randint(0,
                                      self.WINDOW_WIDTH - width_obs)

            obstacle_details.append((width_obs,
                                     height_obs,
                                     location_obs,
                                     location_st_obs))

        return obstacle_details

    def trim_whitespace(self, matrix, details, min_gap):

        if details == -1:
            row = matrix[0, ]
        else:
            row = matrix[matrix.shape[0] - 1, ]

        min_left = np.argmin(row)
        min_right = np.argmin(row[::-1])

        if min_left > min_gap:
            matrix = matrix[:, min_left - min_gap:]

        if min_right > min_gap:
            matrix = matrix[:, 0:len(row) - (min_right - min_gap)]

        return matrix

    def generate_tracks(self):

        obstacles = self.generate_obstacles()

        tracks = []

        for nb_track in range(self.N_TRACKS_GEN):

            # Get Subset of the Obstacles Lists
            new_obs = sample(obstacles, randint(int(self.N_OBSTABLE_GEN / 4),
                                                self.N_OBSTABLE_GEN))

            track = np.hstack(tuple(new_obs))

            x = np.linspace(1, track.shape[1], track.shape[1])
            y = np.linspace(1, track.shape[0] + 1, track.shape[0])
            X, Y = np.meshgrid(x, y)
            output = self.user_function(X, Y)
            shape = output.shape
            bins = np.linspace(output.min(),
                               output.max(),
                               8)  # Eight possible states of Wind
            output = np.digitize(output.flatten(), bins)
            output = output.reshape(shape)

            assert track.shape == output.shape

            for i in range(track.shape[1]):  # X
                for j in range(track.shape[0]):
                    if track[j][i] == -1:
                        output[j][i] = -1

            tracks.append(output)

        return tracks