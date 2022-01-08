import numpy as np
from metric_prefixes import *
from better_round import *

from_prefix_np = np.vectorize(from_prefix)
better_round_np = np.vectorize(better_round)


to_prefix_np = np.vectorize(to_prefix)

def all_to_prefixes(columns, sgns = 2):
      for c in columns.columns:
            if not np.issubdtype(columns[c].dtype, np.number):
                  continue
            columns[c] = to_prefix_np(columns[c], sgns)

def all_better_round(columns, sgns = 2):
      for c in columns.columns:
            if not np.issubdtype(columns[c].dtype, np.number):
                  continue
            columns[c] = better_round_np(columns[c], sgns)
            
