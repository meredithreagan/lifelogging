from smile.common import *
import config

#set up two lists of ids to create image pairs
ids1=[1,2,3,4]
ids2=[5,6,7,8]

#read in the file containing the images
with open("listofimages.txt") as f:
    filenames=f.read().splitlines()
    
#generating the list of image pairs
idPairs=[]
listOfImagePairs=[]
for i in range(0,len(ids1)):
    idPairs.append([ids1[i],ids2[i]])
    listOfImagePairs.append({'stim':[filenames[ids1[i]-1],filenames[ids2[i]-1]], 'dur':6, "trial_num":i+1, "correct_resp":"J"})
print idPairs
print listOfImagePairs
exp=Experiment()

#beginning instructions
Label(text="Press F for the left picture. Press J for the right picture. Press ENTER to begin.")
with UntilDone():
    KeyPress(keys=['ENTER'])

Wait(.5)

#looping though all sets of image pairs
with Loop(listOfImagePairs) as trial:
    Image(source=trial.current['stim'][0], duration=trial.current['dur'])
    Wait(config.BETWEEN_IMAGES_DUR)
    Image(source=trial.current['stim'][1], duration=trial.current['dur'])
    Wait(config.BEFORE_RESP_DUR, jitter=config.BEFORE_RESP_JITTER)
    rsplbl = Label(text="Which photo happened more recently? Press F or J.")
    with UntilDone():
        Wait(until=rsplbl.appear_time)
        ks=KeyPress(keys=config.RESP_KEYS, correct_resp=trial.current['correct_resp'],
                    base_time=rsplbl.appear_time['time'])
    Wait(config.ISI_DUR, jitter=config.ISI_JITTER)

#log trial number, both images, the key response, RT, and correct response
    Log(name="jortask",
        trial_num=trial.current['trial_num'],
        img1=trial.current['stim'][0],
        img2=trial.current['stim'][1],
        resp=ks.pressed,
        rt=ks.rt,
        correct=ks.correct)

exp.run()
