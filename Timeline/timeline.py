# file: relive.py


from smile.common import *
import config
import random


# Define the image information
with open("listofimages.txt") as f:
    filenames = f.read().splitlines()


# Set up a list of image ids.
#ids = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20,
#        21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32]
ids = [1, 2, 3]

# Shuffle the ids.
random.shuffle(ids)

# Construct the stimulus dictionaries
listOfImages = []
for i in range(0,len(ids)):
    listOfImages.append({'stim':filenames[ids[i]-1], 'dur':6, "trial_num":i+1})

# Set up lists defining the post-stimulus questions
labelTexts = ['Which WEEK did this event happen?',
                'Which DAY did this event happen?',
                'Which HOUR did this event happen?']

# Set up lists defining the post-stimulus buttons
weekNames = [1, 2, 3]
dayNames = ['S', 'M', 'Tu', 'W', 'Th', 'F', 'S']
hourNames = ['1a', '2a', '3a', '4a', '5a', '6a', '7a', '8a', '9a', '10a', '11a',
            '12p', '1p', '2p', '3p', '4p', '5p', '6p', '7p', '8p', '9p', '10p',
            '11p', '12a']
nameSets = [weekNames, dayNames, hourNames]
leftPoint, width, topPoint = 300, 1200, 300 # TODO - Fix these so that the buttons are aligned properly



exp=Experiment()


with Loop(listOfImages) as trial:

    # Display the image
    Image(source=trial.current['stim'], duration=trial.current['dur'],
    size_hint_y=None, height=500)
    Wait(config.BEFORE_RESP_DUR, jitter=config.BEFORE_RESP_JITTER)

    # Loop through all the time scales, setting up a line of buttons for each
    # time increment and allowing the user to choose
    responses = {}
    rts = {}
    for i in range(len(nameSets)):

        nameSet = nameSets[i]
        labelText = labelTexts[i]
        spacing = width/len(nameSet)

        with ButtonPress(duration=5) as bp: # TODO - There is an issue with the 24-hour button set. It slows down at runtime. Must bugshoot this!
            MouseCursor()
            for i in range(len(nameSet)):
                name = str(nameSet[i])
                Button(name=name, text=name, center=(leftPoint+i*spacing,
                topPoint), size=(10, 10))
            Label(text=labelText)

        responses.update({name: bp.pressed})
        responses.update({name: bp.rt})

        Wait(.2)

    # Log the responses
    Log(name="relive",
        trial_num=trial.current['trial_num'],
        img=trial.current['stim'],
        resp_week=responses['week']
        resp_day=responses['day']
        resp_hour=responses['hour']
        rt_week=rts['week']
        rt_day=rts['day']
        rt_hour=rts['hour']

exp.run()
