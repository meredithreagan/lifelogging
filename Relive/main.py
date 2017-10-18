
from smile.common import *
import config as Cg
from genstim import gen_stimList
import os


# Information for picking up a run where it left off:
continue_flag = False
starting_block = 1
starting_trial = 1


# Get the stimulus list.
if continue_flag == False:
    # Create stimulus list and back it up to a pickle file.
    imageList = os.listdir('images')

    runs = gen_stimList(imageList=imageList, num_blocks=6, len_blocks=32)

    with open('last_list.pkl', 'wb') as output:
        pickle.dump(runs, output, pickle.HIGHEST_PROTOCOL)
else:
    # Load stimulus list from a pickle file.
    with open('last_list.pkl', 'rb') as _input:
        runs = pickle.load(_input)
    # Truncate stimulus list based on specified starting block/trial.
    runs = runs[starting_block-1:]
    runs[starting_block-1] = runs[starting_block-1][starting_trial-1:]



# Create the experiment instance
exp = Experiment()

Wait(1.0)

# SHOW MAIN INSTRUCTIONS
RstDocument(text=Cg.MAIN_INSTRUCTIONS, width=exp.screen.width*2/3,
            height=exp.screen.height, base_font_size=Cg.RST_FONT_SIZE)
with UntilDone():
    KeyPress(keys=Cg.BUTTON_BOX_KEYS)

Wait(0.5)


with Loop(runs) as block:

    # Check in on the participant
    Label(text="Please wait for the experimenter to \nstart the next block.",
          font_size=Cg.FONT_SIZE, multiline=True, halign="center")
    with UntilDone():
        KeyPress(keys=Cg.RUN_START_KEYS)

    # TR Wait
    Label(text="Please wait.", font_size=Cg.FONT_SIZE)
    with UntilDone():
        studyTR = KeyPress(keys=Cg.TR_KEYS)

    Wait(.5)

    with Loop(block.current) as trial:
	exp.k2pressed = None
	exp.k2base = None
	exp.k2press = None
	exp.k2rt = None

        fixation = Label(text="+", font_size=Cg.FONT_SIZE)
        with UntilDone():
            Wait(duration=Cg.ISI_DUR, jitter=Cg.ISI_JIT)

        image = Image(source=trial.current['stim'], duration=Cg.STIM_DUR,
                      size_hint_y=None, height=500)

        Wait(duration=0.5)

        question1 = Label(text="Did you remember it?\nPress 1 for yes, 2 for no.",
                          font_size=Cg.FONT_SIZE, multiline=True, halign="center")
        with UntilDone():
            Wait(until=question1.appear_time)
            ks1=KeyPress(keys=Cg.YESNO_KEYS, duration=2.0,
                         base_time=question1.appear_time['time'])
	with UntilDone():
	    Wait(2.)

        Wait(duration=0.5)
	with If(ks1.pressed=="1"):
	    question2 = Label(text="Were you able to remember it vividly?\nPress 1 for yes, 2 for no.",
	                      font_size=Cg.FONT_SIZE, multiline=True, halign="center")
	    with UntilDone():
	        Wait(until=question2.appear_time)
	        ks2=KeyPress(keys=Cg.YESNO_KEYS, duration=2.0,
	                     base_time=question2.appear_time['time'])
	    with UntilDone():
    	        Wait(2.)
	    exp.k2pressed = ks2.pressed
	    exp.k2base = ks2.base_time
	    exp.k2press = ks2.press_time
	    exp.k2rt = ks2.rt
	with Else():
	    Wait(2.)
	Wait(.5)

        Log(name="Relive",
            block_num=trial.current['block_num'],
            trial_num_block=trial.current['trial_num_block'],
            trial_num_absolute=trial.current['trial_num_absolute'],
            stim=trial.current['stim'],
            appear=image.appear_time,
            disappear=image.disappear_time,
            block_tr=studyTR.press_time,
            resp_remember=ks1.pressed,
            resp_vivid=exp.k2pressed,
            rt_remember=ks1.rt,
            rt_vivid=exp.k2rt,
            base_remember=ks1.base_time,
            base_vivid=exp.k2base,
            press_remember=ks1.press_time,
            press_vivid=exp.k2press,
            )

    fixation = Label(text="+", font_size=Cg.FONT_SIZE)
    with UntilDone():
        Wait(duration=20.0)


Label(text="The experiment is complete! Please wait!", font_size=Cg.FONT_SIZE)
with UntilDone():
    KeyPress(keys=Cg.RUN_START_KEYS)
exp.run()
