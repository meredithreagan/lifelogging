# file: relive.py


from smile.common import *
import config
import random


# Define the image information
with open("listofimages.txt") as f:
    filenames = f.read().splitlines()


# Set up a list of image ids.
ids = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20,
        21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32]

# Shuffle the ids.
random.shuffle(ids)

listOfImages = []
for i in range(0,len(ids)):
    listOfImages.append({'stim':filenames[ids[i]-1], 'dur':6, "trial_num":i+1})

exp=Experiment()

with Loop(listOfImages) as trial:
    Image(source=trial.current['stim'], duration=trial.current['dur'], size_hint_y=None, height=500)
    Wait(config.BEFORE_RESP_DUR, jitter=config.BEFORE_RESP_JITTER)
    rsplbl1 = Label(text="Did you remember it? Press F for yes, J for no.")
    with UntilDone():
        Wait(until=rsplbl1.appear_time)
        ks1=KeyPress(keys=['F','J'], base_time=rsplbl1.appear_time['time'])
    rsplbl2 = Label(text="Were you able to remember it vividly? Press F for yes, J for no.")
    with UntilDone():
        Wait(until=rsplbl2.appear_time)
        ks2=KeyPress(keys=['F','J'], base_time=rsplbl2.appear_time['time'])
    Wait(config.ISI_DUR, jitter=config.ISI_JITTER)

    Log(name="relive",
        trial_num=trial.current['trial_num'],
        img=trial.current['stim'],
        resp_remember=ks1.pressed,
        resp_vivid=ks2.pressed,
        rt_remember=ks1.rt,
        rt_vivid=ks2.rt)

#log key choice, and image name
exp.run()
