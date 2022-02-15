import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

Octave_Band_I = [10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27]#,28,29,30]
Ocave_Band = [125,250,500,1000,2000,4000]#,8000]
x_ticks_octaveband = ["125", "250", "500", "1k", "2k", "4k"]#, "8k"]
A_weighting = [-16.1, -8.6, -3.2, 0, 1.2, 1]#, -1.1]
I_lst = ["I_Front.csv", "I_Right.csv", "I_Left.csv", "I_Back.csv", "I_Top.csv"]

L_W = [81.8, 77.4, 77.6, 76.2, 78.4]


def _LWLWA():
    sum = 0
    for i, val in enumerate(L_W):
        sum += 10**(0.1*(val))
    LWA = 10*np.log10(sum)
    print(LWA)

_LWLWA()


def _LeqArray(file_lst):
    leq = []
    for i, lst in enumerate(file_lst):
        df  = pd.read_csv(lst, sep=";")
        temp = []
        array= df.to_numpy()
        data = np.transpose(array[:,4].astype(float))
        for x in Octave_Band_I:
            temp.append(data[x])
        leq.append(temp)
    print(leq)
    return leq

def _calculate_log_mean(lst):
    avg = 0
    for i in lst:
        avg += 10**(i / 10)
    return round(10*np.log10(avg / len(lst)),1)

def _calculateOctaveband(lst):
    k=0
    temp = 0
    out = []
    for i in lst:
        if k < 2:
            temp += 10**(0.1 * (i))
            k+=1
        elif k == 2 :
            temp+= 10**(0.1 * (i))
            out.append(10*np.log10(temp))
            temp = 0
            k=0

    print("something")
    print(out)
    return out


def _LW_A(leq):
    leq_T = np.transpose(leq)
    avg_Lp = []
    leq_octave = []

    for i in leq:
        leq_octave.append(_calculateOctaveband(i))
    leq_T2 = np.transpose(np.array(leq_octave))
    print(leq_T2)
    for i in leq_T2:
        LW = _calculate_log_mean(i) + 10 * np.log10(5)
        avg_Lp.append(LW)#_calculate_log_mean(i) + 10*np.log10(5))

    sum = 0
    for i, val in enumerate(avg_Lp):
        sum += 10**(0.1*(val+A_weighting[i]))

    LWA = 10*np.log10(sum)
    return LWA, avg_Lp









def _plotSemilogx(lst, title = ""):
    fig, ax = plt.subplots()
    lst = np.array(lst)

    if lst.ndim == 1:
        ax.semilogx(Ocave_Band, lst+A_weighting)

    else:
        for i, val in enumerate(lst):
           ax.semilogx(Ocave_Band, val, label=" Position {0}".format(i + 1))

    ax.grid(which="major")
    ax.grid(which="minor", linestyle=":")
    ax.set_xlabel("Frequency [Hz]")
    ax.set_ylabel("Amplitude [dB]")
    ax.set_title(title)
    ax.set_xticks(Ocave_Band)
    ax.set_xticklabels(x_ticks_octaveband)
    plt.legend(loc="lower right")

    plt.show()



leq = _LeqArray(I_lst)

LWA, avg_Lpa = _LW_A(leq)
print("LWA: ", LWA)
_plotSemilogx(avg_Lpa)
