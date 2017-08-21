
"""
main v2
"""

import sys

from smile.common import *
from smile.pulse import Pulse

import config
import listgen

# Generate the stimuli.
stimuli = listgen.generate_stim_list()

# Query experimenter whether to continue based on listgen output.
keep_going = raw_input('Stimulus list generated. Continue? y/n: ')
if keep_going != 'y':
    sys.exit()



exp=Experiment()

# SHOW MAIN INSTRUCTIONS
RstDocument(text=config.MAIN_INSTRUCTIONS, width=exp.screen.width*2/3,
            height=exp.screen.height, base_font_size=config.RST_FONT_SIZE)
with UntilDone():
    KeyPress(keys=['ENTER'])

Wait(.5)

#looping though all sets of image pairs
with Loop(stimuli) as block:

    with Loop(block.current) as trial:

        pp = Pulse()

        Wait(config.ISI_DUR, jitter=config.ISI_JITTER)

        #Label(text=trial.current['godModeLabel'], duration=2) ### Only for debugging!
        Image(source=trial.current['first_pres'], duration=config.STIM_DUR,
              size_hint_y=None, height=500)

        Wait(config.BETWEEN_STIMS_DUR)

        Image(source=trial.current['second_pres'], duration=config.STIM_DUR,
              size_hint_y=None, height=500)

        Wait(config.BEFORE_RESP_DUR)

        rsplbl = Label(text="Which happened more recently? Press F for the FIRST image, J for the SECOND image.",
                       font_size=config.FONT_SIZE)
        with UntilDone():
            Wait(until=rsplbl.appear_time)
            ks=KeyPress(keys=config.RESP_KEYS, duration=config.RESP_DUR,
                        correct_resp=trial.current['correctKey'],
                        base_time=rsplbl.appear_time['time'])

        #log trial number, both images, the key response, RT, and correct response
        Log(name="JoR",
            block=trial.current['block'],
            trial_inBlock=trial.current['trial_inBlock'],
            trial_absolute=trial.current['trial_absolute'],
            img1=trial.current['first_pres'],
            img2=trial.current['second_pres'],
            date1=trial.current['first_date'],
            date2=trial.current['second_date'],
            resp=ks.pressed,
            press=ks.press_time,
            base=ks.base_time,
            rt=ks.rt,
            correct=ks.correct,
            listgen_type=trial.current['listgen_type'],
            pulse_on=pp.pulse_on,
            pulse_off=pp.pulse_off)

    Label(text="End of block. When you are ready to continue, press Enter.",
          font_size=config.FONT_SIZE)
    with UntilDone():
        KeyPress(keys=['ENTER'])


Label(text="The experiment is complete! Please notify the experimenter!",
      font_size=config.FONT_SIZE)
with UntilDone():
    KeyPress(keys=['ENTER'])

exp.run()
