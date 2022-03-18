from typing import Union, List, Callable
import random
from . import better_round

Num = Union[int, float]

class dispersed_value:
    value = 0
    disperse = 0

    def __init__(self, v, d):
        self.value = v
        self.disperse = d

    def __repr__(self):
        return '(' + str(self.value) + ' ± ' + str(self.disperse) + ')'

    def __str__(self):
        d = better_round.better_round(self.disperse, 2)
        v = better_round.round_like(self.value, d)
        return '(' + str(v) + ' ± ' + str(d) + ')'

    def __mul__(self, other: Num):
        return dispersed_value(self.value*other, self.disperse*other)

    def __truediv__(self, other: Num):
        return dispersed_value(self.value/other, self.disperse/other)

def experimental_devariate(func: Callable[[Num], Num], x: Num,
                           y: Union[Num, None] = None, dx: Union[Num, None] = None,
                           log: bool = False) -> float: 
    if y is None:
        y = func(x)

    if dx is None:
        dx = 1e-10

    while True:
        dy = func(x + dx) - y
        if log: print('log finding dev: dx, dy: ', dx, dy)
        if dx >= 1e-4:
            if log: print('no diff at large dx, ending…')
            return 0.0
        if abs(dy) < 1e-8:
            dx *= 10
            continue

        if abs(dy) > 1e-7:
            dx /= 10
            continue
        
        return dy/dx
    
def disperse(enable_tuple_input: bool = True,
             enable_tuple_output: bool = False,
             log: bool = False):
    
    """
    Decorator for function to be able work with dispersed values
    (possibly just tuples like "(value, disperse)" )
    """
    
    def act_disperse(func: Callable[..., Num]):
        def dispersed_func(*args, **kw):

            dispersed_args = []
            dispersed_kw = []

            mid_args = list(args)
            mid_kw = kw.copy()
            
            for i in range(len(args)):
                a = args[i]
                if type(a) is dispersed_value or (enable_tuple_input and type(a) is tuple):
                    dispersed_args.append(i)
                    if type(a) is tuple:
                        mid_args[i] = a[0]
                    else:
                        mid_args[i] = a.value

            for i in kw:
                a = kw[i]
                if type(a) is dispersed_value or (enable_tuple_input and type(a) is tuple):
                    dispersed_kw.append(i)
                    
                    if type(a) is tuple:
                        mid_args[i] = a[0]
                    else:
                        mid_kw[i] = a.value
                    
            res = func(*mid_args, **kw)
            disp = 0

            for i in dispersed_args:
                def partial(x):
                    temp = mid_args[i]
                    mid_args[i] = x
                    r = func(*mid_args, **mid_kw)
                    mid_args[i] = temp
                    return r
                
                dev = experimental_devariate(partial, mid_args[i], res)
                c_disp = args[i][1] if type(args[i]) is tuple else args[i].disperse
                if log: print('Counted devariate, delta: ', dev, c_disp)
                disp += (dev * c_disp) ** 2

            for i in dispersed_kw:
                def partial(x):
                    temp = mid_kw[i]
                    mid_kw[i] = x
                    r = func(*mid_args, **mid_kw)
                    mid_kw[i] = temp
                    return r
                
                dev = experimental_devariate(partial, mid_kw[i], res)
                c_disp = kw[i][1] if type(kw[i]) is tuple else kw[i].disperse
                if log: print('Counted devariate, delta: ', dev, c_disp)
                disp += (dev * c_disp) ** 2

            if disp != 0:
                disp = disp**0.5
                if enable_tuple_output:
                    return (res, disp)
                
                return dispersed_value(res, disp)
            else:
                return res
            
        return dispersed_func
    
    return act_disperse
