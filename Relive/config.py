
import os

_ins_path = "instructions"
_main_ins_filename = "main_instruct.rst"

MAIN_INSTRUCTIONS = open(os.path.join(_ins_path,
                                      _main_ins_filename)).read()


FONT_SIZE = 35
RST_FONT_SIZE = 35
LOC_STIM_DUR = 0.500
LOC_INTER_STIM_DUR = 0.500


STIM_DUR = 6.
RESP_DUR = 2.0
ISI_DUR = 2.0
ISI_JIT = 2.0

MAIN_NUM_BLOCKS = 5
MAIN_NUM_TARGETS = 30

BUTTON_BOX_KEYS = ["1", "2", "3", "4"]#["_1", "_2", "_3", "_4"]
YESNO_KEYS = ["1", "2"]#["_1", "_2"]
TR_KEYS = ["5"]#["_5"]
RUN_START_KEYS = ["0"]

MD_NUM_VAR = 3
MD_DUR = 20
MD_PRAC_DUR = 12
MD_PAM = True  # plus AND minus?
MD_KEYS = {'True': BUTTON_BOX_KEYS[0],
           'False': BUTTON_BOX_KEYS[1]}

################################################################################S


