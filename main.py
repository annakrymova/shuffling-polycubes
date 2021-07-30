

import os
import numpy as np
from pathlib import Path
from datetime import datetime
from functions import read_value, read_int, grow_model
import cProfile
from line_profiler import LineProfiler

print('Welcome to Shuffling Polycubes Model!')

print('Do you want a picture of your model? (with a large model it can take time)  \n0 -- no \n1 -- yes')
pic = bool(read_value([0, 1]))
# pic = bool(1)

print('How many models would you like to build?')
num_models = read_int()
# num_models = 1

print('Do you want to start with a worm or with a box?'
      '\n 0 -- with a box'
      '\n 1 -- with a worm')
shape = bool(read_value([0, 1]))
# shape = bool(0)
if shape:
    shape_str = 'worm'
else:
    shape_str = 'box'

if shape:
    print('What is polyomino size?')
else:
    print('What is polyomino size?'
          '\n it has to be a natural number cube')
size = read_int()
# size = 64

print('How many shuffles fo you want?')
# t = read_int()
t = 10*size**3

# lp = LineProfiler()
# lp_wrapper = lp(grow_model)
# lp_wrapper(size, t, shape)
# lp.print_stats()

for q in range(num_models):
    print("WORKING ON MODEL #"+str(q+1))
    now = datetime.now()
    dt_string = now.strftime("%d:%m:%Y_%H.%M.%S")
    folder_name = str(size)+'/'+str(t)+'_'+shape_str+'_'+dt_string
    os.makedirs(folder_name)
    Process = grow_model(size, t, shape)
    f = open(folder_name+"/MAYA_pr.txt", "w+")
    f.write("import maya.cmds as cmds \nimport math as m \n"
            "import os,sys \nEden = " + str(Process)+"\nt = len(Eden)"
            "\nfor i in range(0,t):\n\taux = cmds.polyCube()"
            "\n\tcmds.move(Eden[i][0],Eden[i][1],Eden[i][2],aux)")
    f.close()
    a = 10
