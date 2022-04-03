import numpy as np
from . import metric_prefixes
from . import better_round
from . import disperse

from_prefix_np = np.vectorize(metric_prefixes.from_prefix)
better_round_np = np.vectorize(better_round.better_round)
round_error_np = np.vectorize(better_round.round_error)
to_prefix_np = np.vectorize(metric_prefixes.to_prefix)
create_dispersed_array = np.vectorize(disperse.dispersed_value)
# def skip_non_num(func):

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


def array_disperse(func):
    """
    Much simpier version of disperse, but able to manage numpy arrays
    Inteprets all params (no keywords!) that look like (a, b) as value - error
    """
        
    actual_func = np.vectorize(disperse.disperse()(func))
    
    def new_func(*args):
        args = list(args)
        for i in range(len(args)):
            if type(args[i]) == tuple and len(args[i]) == 2:
                args[i] = create_dispersed_array(*args[i])
                
        return actual_func(*args)

    return new_func