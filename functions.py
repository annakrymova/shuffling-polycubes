import random
import matplotlib.pyplot as plt
from tqdm import tqdm
import itertools
import gudhi as gd
import numpy as np
from numpy import linalg as la
import collections
import matplotlib.patches as mpatches
from scipy.optimize import curve_fit
from line_profiler import LineProfiler

def read_value(arr):
    while True:
        try:
            x = int(input())
            if x not in arr:
                raise ValueError
            break
        except ValueError:
            print("Oops!  That was no valid number.  Try again...")
    return x

def read_int():
    while True:
        try:
            x = int(input())
            break
        except ValueError:
            print("Oops!  That was no valid number.  Try again...")
    return x

def grow_model(size, t, shape):
    if shape:
        model, perimeter, process = start_worm(size)
    else:
        model, perimeter, process = start_cube(size)

    pbar = tqdm(total=t)
    pbar.update(1)
    steps = 0
    sh = shift()

    while steps < t:
        tile_selected = random.choice(process)
        # new_perimeter = perimeter.copy()
        process.remove(tile_selected)
        neighb = neighbours(tile_selected, sh)
        removed = []
        for x in neighb:
            if x in perimeter:
                remains = False
                for y in neighbours(x, sh):
                    if y in process:
                        remains = True
                        break
                if not remains:
                    perimeter.remove(x)
                    removed += [x]
        perimeter += [tile_selected]
        new_tile = random.choice(perimeter)
        process += [new_tile]

        connected_bfs = is_connected(process, tile_selected, new_tile, sh)
        # connected = len(return_cc(process, sh)) == 1
        if not connected_bfs:
            """put cube back on its place"""
            process += [tile_selected]
            process.remove(new_tile)
            perimeter.remove(tile_selected)
            perimeter += removed
            continue

        model[tile_selected][0] = 0
        model[new_tile][0] = 1
        perimeter.remove(new_tile)

        for x in neighbours(new_tile, sh):
            if x not in process and x not in perimeter:
                perimeter += [x]
                model[x] = [0]
        steps += 1
        pbar.update(1)
    return process

def start_worm(s):
    model = {}
    process = []
    perimeter = []
    range_cubes = range(-int(s/2), int(s/2)+int(s % 2 == 1))
    for j in range_cubes:
        cell = (j, 0, 0)
        model[cell] = [1]
        process += [cell]
        neighbours = [(j, 1, 0), (j, -1, 0), (j, 0, 1), (j, 0, -1)]
        perimeter += neighbours
    perimeter += [(range_cubes[0]-1, 0, 0), (range_cubes[-1]+1, 0, 0)]
    for x in perimeter:
        model[x] = [0]
    return model, perimeter, process

def start_cube(s):
    len = round(s ** (1./3))
    model = {}
    process = []
    perimeter = []
    range_cubes = range(-int(len/2), int(len/2)+int(s % 2 == 1))
    for j in range_cubes:
        for i in range_cubes:
            for k in range_cubes:
                cell = (j, i, k)
                model[cell] = [1]
                process += [cell]
                if j == range_cubes[-1]:
                    perimeter += [(j+1, i, k)]
                if j == range_cubes[0]:
                    perimeter += [(j-1, i, k)]
                if i == range_cubes[-1]:
                    perimeter += [(j, i+1, k)]
                if i == range_cubes[0]:
                    perimeter += [(j, i-1, k)]
                if k == range_cubes[-1]:
                    perimeter += [(j, i, k+1)]
                if k == range_cubes[0]:
                    perimeter += [(j, i, k-1)]
    for x in perimeter:
        model[x] = [0]
    return model, perimeter, process

def neighbours(tile, sh):
    neighb = []
    for x in sh:
        neighb.append(tuple(tile+x))
    return neighb

"""CONNECTED COMPONENTS"""
def is_connected(tiles, tile_selected, new_tile, sh):
    cc = [[x] for x in neighbours(tile_selected, sh) if x in tiles]
    num_cc = len(cc)
    merged = [False]*num_cc
    finished = [False]*num_cc
    num_iter = 0
    connected = False
    while sum(finished) < num_cc and sum(merged) < num_cc - 1:
        for i in range(num_cc):
            if not merged[i] and not finished[i]:
                cube_selected = cc[i][num_iter]
                for x in [y for y in neighbours(cube_selected, sh) if y in tiles]:
                    if x not in cc[i]:
                        cc[i] += [x]
                    for j in range(num_cc):
                        if j != i and x in cc[j]:
                            merged[max(i, j)] = True
                            finished[max(i, j)] = True
                if (num_iter + 1) == len(cc[i]):
                    finished[i] = True
        num_iter += 1
    if sum(merged) == num_cc-1:
        connected = True
    return connected

"""CONNECTED COMPONENTS"""
def return_cc(tiles, shift):
    # pbar = tqdm(total=len(tiles))
    pbar = 0
    cc = []
    visited = dict(zip(tiles, [False]*len(tiles)))
    for tile in tiles:
        if not visited[tile]:
            temp = []
            cc.append(bfs(tiles, temp, tile, visited, shift, pbar))
    return cc

def bfs(tiles, temp, tile, visited, shift, pbar):
    visited[tile] = True
    # pbar.update(1)
    temp.append(tile)
    nearest_tiles = np.array(tile)+shift
    neighbours = [tuple(x) for x in nearest_tiles if tuple(x) in tiles]
    for v in neighbours:
        if not visited[v]:
            temp = bfs(tiles, temp, v, visited, shift, pbar)
    return temp

def shift():
    shift = []
    for i in range(3):
        x = np.zeros((3,), dtype=int)
        x[i] = 1
        shift.append(x)
        y = np.zeros((3,), dtype=int)
        y[i] = -1
        shift.append(y)
    return shift

def shift():
    sh = []
    for i in range(3):
        x = np.zeros((3,), dtype=int)
        x[i] = 1
        sh.append(x)
        y = np.zeros((3,), dtype=int)
        y[i] = -1
        sh.append(y)
    return sh


