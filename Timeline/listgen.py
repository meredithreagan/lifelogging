

import glob
import random
from smile.common import *
import config
import os

def listgen(block_num=8, block_length=24):

    data_dir = os.path.join("images", "*")

    paths = []
    for x in glob.glob(data_dir):
        m = glob.glob(os.path.join(x, "morning", "*"))
        for i in m:
            paths.append(i)
        a = glob.glob(os.path.join(x, "afternoon", "*"))
        for i in a:
            paths.append(i)

    # randomize the images
    random.shuffle(paths)

    blocks = []
    trialCounter = 0
    for i in range(block_num):
        block = []
        for j in range(block_length):
            trialCounter += 1
            stimPath = paths.pop()
            block.append({'stim': stimPath,
                          'block': i+1,
                          'trial_inBlock': j+1,
                          'trial_absolute': trialCounter})
        blocks.append(block)

    #print blocks
    return blocks
