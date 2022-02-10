import numpy as np


po = 20*(10**(-5))
def _getPressure(val1, val2):
    return po*(10**(val1 / 10)), po*(10**(val2 / 10))

def _calculate_mean(val1, val2, val3):
    x = _getPressure(val1)
    yy = x
    xx = x
    val22 = val2
    val11 = val1
    avg = (yy - xx) / (val22 - val11)
    avg_db = round(10*np.log10((avg / po)),1)
    print(avg_db)

def _calculate_log_mean(lst):
    avg_db = 0
    for i, val in enumerate(lst):
        if(i<len(lst)-1):
            if(i == 0): val1 = val
            else : val1 = avg_db
            val2 = lst[i+1]
            x, y = _getPressure(val1, val2)
            avg = (y-x) / (val2 - val1)
            avg_db = round(10*np.log10((avg / po)),1)
    print(avg_db)




#_calculate_mean(70, 60, 60)

_calculate_log_mean([60,70])

#print (3 / 2)