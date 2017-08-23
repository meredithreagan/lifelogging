
import random
import config as Cg


# LISTGEN
def gen_stimList(imageList, num_blocks, len_blocks):
    # Set up a shuffled list of image ids
    ids = range(1, len(imageList)+1)
    random.shuffle(ids)
    print ids

    # Fill out a list of lists of dictionaries based on the image id list
    listOfBlocks = []
    imageIndex = 0
    for n in range(num_blocks):
        block = []
        for i in range(len_blocks):
            #temp = {'stim': os.path.join(Cg.STIM_PATHS, temp)}
            block.append({'stim':'images/'+imageList[ids[imageIndex]-1],
            "trial_num_block":i+1, "trial_num_absolute":imageIndex+1,
            'block_num':n+1})
            imageIndex += 1
        listOfBlocks.append(block)
    return listOfBlocks

