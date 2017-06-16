from smile.common import *
import config
ids1=[1,2,3,4]
ids2=[5,6,7,8]
with open("listofimages.txt") as f:
    filenames = f.read().splitlines()

idPairs=[]
listOfImagePairs=[]
for i in range(0,len(ids1)):
    idPairs.append([ids1[i],ids2[i]])
    listOfImagePairs.append({'stim':[filenames[ids1[i]-1],filenames[ids2[i]-1]], 'dur':3, "trial_num":i+1})

exp=Experiment()

Label(text="Press J for the left picture. Press K for the right picture. Press ENTER to begin.")
with UntilDone():
    KeyPress(keys=['ENTER'])

Wait(.5)

with Loop(listOfImagePairs) as trial:
    Image(source=trial.current['stim'][0], duration=trial.current['dur'])
    Wait(config.BETWEEN_IMAGES_DUR)
    Image(source=trial.current['stim'][1], duration=trial.current['dur'])
    Wait(config.BEFORE_RESP_DUR, jitter=config.BEFORE_RESP_JITTER)
    rsplbl = Label(text="Which photo happened more recently? Press J or K.")
    with UntilDone():
        Wait(until=rsplbl.appear_time)
        ks=KeyPress(keys=['J','K'], correct_resp=trial.current['correct_resp'],
                    base_time=rsplbl.appear_time['time'])
    Wait(config.ISI_DUR, jitter=config.ISI_JITTER)
    Log(name="jortask",
        trial_num=trial.currenat['trial_num'],
        img1=trial.current['stim'][0],
        img2=trial.current['stim'][1],
        resp=ks.pressed,
        rt=ks.rt,
        correct=ks.correct)
#log key choice, and image name
exp.run()
