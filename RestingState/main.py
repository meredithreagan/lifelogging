
from smile.common import *
import config as Cg
import os




exp = Experiment()


# TR WAIT
Label(text="Please wait.", font_size=Cg.FONT_SIZE)
with UntilDone():
    studyTR = KeyPress(keys=Cg.TR_KEYS)

# RESTING STATE FOR 7 MINUTES
Label(text=" ", font_size=Cg.FONT_SIZE)
with UntilDone():
    Wait(420.)

Log(name="RestingState",
    block_tr=studyTR.press_time
    )



Label(text="Please wait.", font_size=Cg.FONT_SIZE)
with UntilDone():
    KeyPress(keys=Cg.RUN_START_KEYS)

exp.run()
