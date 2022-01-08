from better_round import better_round

prefixes = {'K': 3,
            'M': 6,
            'G': 9,
            'T': 12,
            'm': -3,
            'μ': -6,
            'n': -9}

def from_prefix(string):
      if string[-1] in prefixes:
            return float(string[:-1])*10**prefixes[string[-1]]
      
      return float(string)

def to_prefix(number, signs = None):
      if number == 0:
            return '0'
      
      if signs != None:
            number = better_round(number, signs)
            
      m = np.log10(abs(number))
      max_ = ''
      max_mult = 0
      for p in prefixes:
            v = prefixes[p]
            # print(m, v, v*m > 0, m - v < 3, m - v > 0)
            if v*m > 0 and m - v < 3 and m - v >= 0:
                  if abs(v) > abs(max_mult):
                        max_mult = v
                        max_ = p
      if signs == None:
            return str(round(number/10**max_mult, 9)) + max_
      else:
            return str(better_round(number/10**max_mult, signs)) + max_

