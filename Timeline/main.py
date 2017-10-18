
import pickle

from smile.common import *
from smile.pulse import Pulse

import config
from listgen import listgen



# Information for picking up a run where it left off: ######################################################################################## REPLICATE
continue_flag = False
starting_block = 1
starting_trial = 1


# Get the stimulus list. ######################################################################################## REPLICATE
if continue_flag == False:
    # Create stimulus list and back it up to a pickle file.
    stimuli = listgen()
    with open('last_list.pkl', 'wb') as output:
        pickle.dump(stimuli, output, pickle.HIGHEST_PROTOCOL)
else:
    # Load stimulus list from a pickle file.
    with open('last_list.pkl', 'rb') as _input:
        stimuli = pickle.load(_input)
    # Truncate stimulus list based on specified starting block/trial.
    stimuli = stimuli[starting_block-1:]
    stimuli[starting_block-1] = stimuli[starting_block-1][starting_trial-1:]



# Create new experiment instance.
exp = Experiment()

# Show main instructions.
RstDocument(text=config.MAIN_INSTRUCTIONS, width=exp.screen.width*2/3,
            height=exp.screen.height, base_font_size=config.RST_FONT_SIZE)
with UntilDone():
    KeyPress(keys=['ENTER'])

Wait(2)



with Loop(stimuli) as block:

    with Loop(block.current) as trial:

        pp = Pulse()

        Wait(config.ISI_DUR, jitter=config.ISI_JITTER)

        with Parallel():
            img = Image(source=trial.current['stim'], top=exp.screen.top+5,
                        trial_num=trial.current['trial_absolute'],
                        size_hint_y=None, height=500)

        with UntilDone():
            with Serial():
                with Parallel():

                    MouseCursor()
                    s1 = Slider(min=0, max=3, value=-100, width=config.SLIDER_WIDTH, top=400, padding=0)

                    increments = [0, 1, 2, 3]
                    names = ['Week 1', 'Week 2', 'Week 3']
                    for increment in increments:
                        Rectangle(color='white', top=375, width=2, height=50, center_x=s1.left+increment*(config.SLIDER_WIDTH/3))
                        if increment != max(increments):
                            Label(text=names[increment], center_x=(s1.left)+config.SLIDER_WIDTH/(6)+increment*config.SLIDER_WIDTH/(3), top=340)

                    mbs1=MouseButton(widget=s1)

                with UntilDone():
                    Wait(until=mbs1)
                    s1.disabled = True

                    with Parallel():
                        line1=Rectangle(color='red', top=350, width=config.SLIDER_WIDTH, height=1, center_x=s1.center_x,)
                        MouseCursor()
                        s2 = Slider(min=0, max=7, value=-100, width=config.SLIDER_WIDTH, top=300,padding=0)

                        increments = [0, 1, 2, 3, 4, 5, 6, 7]
                        names = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
                        for increment in increments:
                            Rectangle(color='white', top=275, width=2, height=50, center_x=s1.left+increment*((config.SLIDER_WIDTH/7)*1.003))
                            if increment != max(increments):
                                Label(text=names[increment], center_x=(s2.left)+config.SLIDER_WIDTH/(14)+increment*config.SLIDER_WIDTH/(7), top=240)

                        mbs2=MouseButton(widget=s2)

                    with UntilDone():
                        Wait(until=mbs2)
                        s2.disabled = True

                        with Parallel():
                            line2=Rectangle(color='red', top=250, width=config.SLIDER_WIDTH, height=1, center_x=s2.center_x)
                            MouseCursor()
                            s3 = Slider(min=0, max=24, value=-100, width=config.SLIDER_WIDTH, top=200, padding=0)

                            increments = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24]
                            names = ['12a', '1a', '2a', '3a', '4a', '5a', '6a', '7a', '8a', '9a', '10a', '11a', '12p', '1p', '2p', '3p', '4p', '5p', '6p', '7p', '8p', '9p', '10p', '11p', '12a']
                            for increment in increments:
                                Rectangle(color='white', top=175, width=2, height=50, center_x=s3.left+increment*(config.SLIDER_WIDTH/24))
                                Label(text=names[increment], center_x=(s3.left)+increment*config.SLIDER_WIDTH/(24), top=120)

                            mbs3=MouseButton(widget=s3)

                        with UntilDone():
                            Wait(until=mbs3)
                            s3.disabled = True

                            with Parallel():
                                line3=Rectangle(color='red', top=150, width=config.SLIDER_WIDTH, height=1, center_x=s3.center_x)
                                MouseCursor()
                                s4 = Slider(min=0, max=10, value=-100, width=config.SLIDER_WIDTH, top=100, padding=0)
                                #conf0=Rectangle(color='white', top=75, width=2, height=50, center_x=s4.left+100)
                                #conf1=Rectangle(color="white", top=75, width=2, height=50, center_x=s4.right-100)
                                lblvconf = Label(text="<--- Not at all confident", center_x=s4.left+100, top=40)
                                lblnotconf = Label(text="Very confident --->", center_x=s4.right-100, top=40)
                                mbs4=MouseButton(widget=s4)

                            with UntilDone():
                                Wait(until=mbs4)
                                s4.disabled = True

        Log(name="timeline",
            block=trial.current['block'],
            trial_inBlock=trial.current['trial_inBlock'],
            trial_absolute=trial.current['trial_absolute'],
            stim=trial.current['stim'],
            value_chosen_1=s1.value,
            value_chosen_2=s2.value,
            value_chosen_3=s3.value,
            value_chosen_4=s4.value,
            pulse_on=pp.pulse_on,
            pulse_off=pp.pulse_off)

    Label(text="End of block. When you are ready to continue, press Enter.")
    with UntilDone():
        KeyPress(keys=['ENTER'])

Label(text="The experiment is complete! Please notify the experimenter!",
      font_size=config.FONT_SIZE)
with UntilDone():
    KeyPress(keys=['ENTER'])

exp.run()
