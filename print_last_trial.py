
import os
import sys

import pandas as pd
from smile.log import log2dl


slog_name = sys.argv[1]


df = pd.DataFrame(log2dl(slog_name))
print 'Last (absolute) trial to be FINISHED was:', len(df.index)
