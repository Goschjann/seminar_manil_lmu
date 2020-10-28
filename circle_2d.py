#!/usr/bin/env python
# inspired by de la porte 2008: An Introduction to Diffusion Maps
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
from math import atan2, atan, degrees
import math
import argparse
import pdb
import copy
import os

def parse_args():
    parser = argparse.ArgumentParser(description='Circle plots')
    parser.add_argument('--nrows', type=int, default=127,
                        help='pixels of the image')
    parser.add_argument('--n', type=int, default=300,
                        help='max amount of plots to make')
    parser.add_argument('--delta', type=int, default=150,
                        help='delta for the clock hands distance, the larger the greater the stripe')
    parser.add_argument('--edge', type=int, default=1,
                        help='which edge position to use for the clock hands as fix point')
    return parser.parse_args()

########
# Helpers
########

def is_edge_pixel(array, coordinate):
    # find coordinates of edge pixels on the circle
    # and store their coordinates
    # egde pixels have max 3 neighbor pixels (without diagonals
    if array[coordinate[0] - 1, coordinate[1]] == 0.0 and array[coordinate[0] + 1, coordinate[1]] == 0.0 and array[coordinate[0], coordinate[1] - 1] == 0.0 and array[coordinate[0], coordinate[1] + 1] == 0.0:
        return False
    elif array[coordinate[0], coordinate[1]] != 0.0:
        return False
    else:
        return True

def point_on_line(array, center, edge, point, delta):
    # tells us which point in the array lies on the line between center and edge
    # used to draw the clock hands in the images

    # absolute distance point from the line between center, edge point
    d = abs(np.cross(np.asarray(point) - np.asarray(center), np.asarray(edge) - np.asarray(center)))

    # select only those points that are in the same quadrant as edge
    if edge[0] <= center[0] and edge[1] <= center[1] and point[0] <= center[0] and point[1] <= center[1] or \
        edge[0] <= center[0] and edge[1] >= center[1] and point[0] <= center[0] and point[1] >= center[1] or \
        edge[0] >= center[0] and edge[1] <= center[1] and point[0] >= center[0] and point[1] <= center[1] or \
        edge[0] >= center[0] and edge[1] >= center[1] and point[0] >= center[0] and point[1] >= center[1]:
        between = True
    else:
        between = False

    if d <= delta and between :
        return True
    else:
        return False

def draw_clock_hands(array, center, edge, delta):
    for i in range(array.shape[0]):
        for j in range(array.shape[0]):
            if array[i, j] == 0.0 and point_on_line(array=array, center=center, edge=edge, point=(i, j), delta=delta):
                array[i, j] = 1.0
    return array

#######
## Main function
#######

def generate_circle_data(args):
    args = parse_args()
    radius = int(args.nrows/2)
    centroid = int(np.median(np.arange(args.nrows)))
    center = np.asarray((centroid, centroid))
    arr = np.ones(shape=(args.nrows, args.nrows))

    # create results folder
    if not os.path.exists('circle_data'):
        os.mkdir('circle_data')

    # fill the circle with 0's
    for i in range(args.nrows):
        for j in range(args.nrows):
            if abs((j - centroid)**2 + (i - centroid)**2) < radius**2 :
                arr[i, j] = 0.0

    # select the edges of the circle as we want to walk alongside them
    # calculate angle to centroid line as 'label'
    # aka angle coordinate_centroid,coordinate_centroid_right - coordinate_centroid,edge
    C = (centroid, centroid)
    C_r = (centroid, centroid + radius)

    edges = []
    y = []
    for i in range(1, args.nrows-1):
        for j in range(1, args.nrows-1):
            if is_edge_pixel(array=arr, coordinate=(i, j)):
                edges.append((i, j))
                # calculate angles as y
                # need the atan2 built upon sin and cos vor value range [0, 360]
                # https://math.stackexchange.com/questions/878785/how-to-find-an-angle-in-range0-360-between-2-vectors
                RC = np.asarray((C_r[0] - C[0], C_r[1] - C[1]))
                EC = np.asarray((i - C[0], j - C[1]))

                dot = np.dot(RC, EC)
                det = np.linalg.det(np.concatenate([RC.reshape(-1, 1), EC.reshape(-1, 1)], 1))
                angle = degrees(math.atan2(det, dot))

                y.append(angle)


    # sort edges by y
    edges = [edge for _, edge in sorted(zip(y,edges))]
    print(f'{len(edges)} edge points')

    edge_idx_list = [int(foo) for foo in np.linspace(0, len(edges) - 1, args.n)]
    # plot only 10 circles
    plot_idx = [int(idx) for idx in np.linspace(start=0, stop=len(edges) - 1, num=10)]
    store_idx = 0
    rawdata_list = []
    for idx in edge_idx_list:
        # get array with clockhands
        blank = copy.deepcopy(arr)
        arr_clockh = draw_clock_hands(array=blank, center=center, edge=edges[idx], delta=args.delta)

        # store the rawdata of the plot as vetor
        rawdata_list.append(arr_clockh.reshape(-1, 1))

        # store the plot
        if idx in plot_idx:
            plt.close()
            plt.imsave(fname=f'circle_data/circle_clockh_{store_idx}.png', arr=arr_clockh, dpi=150, cmap='gray')
            store_idx += 1

    # store rawdata in row-format as .csv
    rawdata = pd.DataFrame(np.concatenate(rawdata_list, 1).transpose())
    rawdata.columns = [f'x_{idx}' for idx in range(rawdata.shape[1])]
    rawdata['y'] = pd.DataFrame(y)
    rawdata.to_csv('circle_data/rawdata_circle.csv')

if __name__ == "__main__":
    args = parse_args()
    generate_circle_data(args=args)