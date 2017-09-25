
import os

_ins_path = "instructions"
_main_ins_filename = "main_instruct.rst"

MAIN_INSTRUCTIONS = open(os.path.join(_ins_path,
                                      _main_ins_filename)).read()

FONT_SIZE=30
RST_FONT_SIZE=30
BETWEEN_STIMS_DUR=1
STIM_DUR=3
BEFORE_RESP_DUR=1
RESP_KEYS=['F','J']
RESP_DUR=3
ISI_DUR=2
ISI_JITTER=2
RESP_DELAY=1
