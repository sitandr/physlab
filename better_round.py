import math

def better_round(x, signs):
      
      if x == 0:
            return 0
      
      m = signs - 1 - int(math.floor(math.log10(abs(x))))
      return round(x, m) if m > 0 else int(round(x, m))

def round_like(to_round, rounded):
    n = 0
    diff = round(rounded) != rounded
    p = diff * 2 - 1
    while p == (round(rounded, n + p) != rounded) * 2 - 1:
        n += p
    n += diff
    return round(to_round, n)
    
