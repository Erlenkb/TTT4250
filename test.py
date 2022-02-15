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
            #x, y = _getPressure(val1, val2)

            x = 10**6
            y = 10**7

            avg = (x-y) / ((6 - 7))
            avg_db = round(10*np.log10(avg),1)
    print(avg_db)


test_arr = [1,1,1,1,1,1,1]
nparr = np.array(test_arr)
print("shape =",np.shape(nparr))
shape = np.shape(nparr)

array = np.array([[1,2,3,4],[5,6]])
print(" ##########", array[0])
#print(array[1][1])
#array = np.zeros((2,4))
#print(array)
#print("shape0 = {}, shape1 = {}".format(array.shape[0], array.shape[1]))
#_calculate_mean(70, 60, 60)

print(_calculate_log_mean([60,61]))
print("#####", (2*0.465*0.25)+(2*0.3*0.25)+0.3*0.465)
print("######",(2*2.465*1.25)+(2*2.03*1.25)+(2.465*2.03))
#print (3 / 2)