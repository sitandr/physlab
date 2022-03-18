import numpy as np
from . import metric_prefixes
from . import better_round
from . import disperse

from_prefix_np = np.vectorize(metric_prefixes.from_prefix)
better_round_np = np.vectorize(better_round.better_round)
round_error_np = np.vectorize(better_round.round_error)

to_prefix_np = np.vectorize(metric_prefixes.to_prefix)

def all_to_prefixes(columns, sgns = 2):
      for c in columns.columns:
            if not np.issubdtype(columns[c].dtype, np.number):
                  continue
            columns[c] = to_prefix_np(columns[c], sgns)
            
      return columns

def all_better_round(columns, sgns = 2):
      for c in columns.columns:
            if not np.issubdtype(columns[c].dtype, np.number):
                  continue
            columns[c] = better_round_np(columns[c], sgns)
      
      return columns

def all_round_error(columns):
      for c in columns.columns:
            if not np.issubdtype(columns[c].dtype, np.number):
                  continue
            columns[c] = round_error(columns[c])
            
      return columns