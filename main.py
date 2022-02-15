import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


##Global
x_ticks_octaveband = ["16","31.5","63","125", "250", "500", "1k", "2k", "4k", "8k", "16k"]
A_weighting = [-56.7, -39.4, -26.2, -16.1, -8.6, -3.2, 0, 1.2, 1, -1.1, -4]
Octave_bands = [16,31.5,63,125,250,500,1000,2000,4000,8000,16000]
Octave_bands2 = [125,250,500,1000,2000,4000,8000]
po = 20*(10**(-5))

##Metode 1
Header_list = ["Name","Start", "Time","Duration","Unit","LAeq",	"LAFmax","LAFmin","LAE","LApeak","LCeq","LCFmax","LCFmin","LCE","LCpeak","LZeq","LZFmax","LZFmin","LZE","LZpeak","Lfeq 16 Hz","Lfeq 31.5 Hz","Lfeq 63 Hz", "Lfeq 125 Hz", "Lfeq 250 Hz", "Lfeq 500 Hz", "Lfeq 1 kHz", "Lfeq 2 kHz", "Lfeq 4 kHz", "Lfeq 8 kHz", "Lfeq 16 kHz", "LfFmax 16 Hz", "LfFmax 31.5 Hz", "LfFmax 63 Hz", "LfFmax 125 Hz", "LfFmax 250 Hz", "LfFmax 500 Hz", "LfFmax 1 kHz", "LfFmax 2 kHz", "LfFmax 4 kHz", "LfFmax 8 kHz", "LfFmax 16 kHz", "LfFmin 16 Hz", "LfFmin 31.5 Hz", "LfFmin 63 Hz", "LfFmin 125 Hz", "LfFmin 250 Hz", "LfFmin 500 Hz", "LfFmin 1 kHz", "LfFmin 2 kHz", "LfFmin 4 kHz", "LfFmin 8 kHz", "LfFmin 16 kHz", "LfE 16 Hz", "LfE 31.5 Hz", "LfE 63 Hz", "LfE 125 Hz", "LfE 250 Hz", "LfE 500 Hz", "LfE 1 kHz", "LfE 2 kHz", "LfE 4 kHz", "LfE 8 kHz", "LfE 16 kHz"]
Positions = ["1","1","1","2","2","2","3","3","3","4","4","4","5","5","5",]
Test_type = ["Background","Reference","Test","Test","Reference","Background","Background","Test","Reference","Background","Test","Reference","Background","Test","Reference"]
L_W_RSS = [79.8, 81, 80.9, 84.9, 85.1, 82.7,  79.2] # 125 - 8000Hz
r_rss = [1.524, 2.48, 2.899, 3.469, 2.22]
r_ts = [1.752 , 2.284, 2,44, 4.02, 2.139]

room_size = [8.501, 6.042, 5.174]
M2_box = [0.465+2,0.3+2,0.25+1]
M3_box = [0.465+0.56,0.307+0.56,0.25+0.28]


Background_noise_M1 = [0,5,6,9,12]
Test_source_M1 = [2,3,7,10,13]
Reference_source_M1 = [1,4,8,11,14]

#Metode 2
Sides = ["Front", "Right", "Left", "Back", "Top"]
Method_2 = [15,16,17,18,19]


########################## Define what you want to plot ################
back = False
test = True
ref = True
M2 = True
Noise_Val = 4
M = 2 # 0 = M1, 1 = M2, 2 = M1 & M2




#######################################################################

####  Method 1

def _LeqArray(file):
    df = pd.read_csv(file, sep=";")
    array = df.to_numpy()
    Data_Arrray = array[:,22:29].astype(np.float)
    noise = []
    for i in Background_noise_M1 : noise.append(array[i,Noise_Val])
    return noise, Data_Arrray

def _M2LAeq():
    df = pd.read_csv("Trykk_Lab1.csv", sep=";")
    array = df.to_numpy()
    Data = array[:,4].astype(np.float)
    out = []
    for i in Method_2 : out.append(Data[i])
    return np.array(out)

def _getPressure(val1, val2):
    return 10**(val1 / 10), 10**(val2 / 10)

def _calculate_log_mean(lst):
    avg = 0
    for i in lst:
        avg += 10**(i / 10)
    return round(10*np.log10(avg / len(lst)),1)




def _createLpiB(noise):
    LpiBLP = _calculate_log_mean(noise)
    print("########",LpiBLP)
    return LpiBLP,

def _calculateLpiRSS(ref,LpiB, plot=False):
    LpiRSS = []
    for i, val in enumerate(ref):
        temp = []
        for y, val2 in enumerate(val):
            temp.append(round(10*np.log10((10**(val2 / 10)) - 10**(LpiB[y] / 10)),1))
        LpiRSS.append(temp)
    if plot : _plotSemilogx(LpiRSS)

    return LpiRSS

def _calculateLpiST(ST, LpiB, plot=False):
    LpiST = []
    for i, val in enumerate(ST):
        temp = []
        for y,val2 in enumerate(val):
            temp.append(round(10 * np.log10((10 ** (val2 / 10)) - 10 ** (LpiB[y] / 10)),1))
        LpiST.append(temp)
    if plot : _plotSemilogx(LpiST)
    return LpiST

def _plotSemilogx(lst, DeltaLf=False, title = ""):
    fig, ax = plt.subplots()
    lst = np.array(lst)


    if lst.ndim == 1:
        a_weighted = lst + A_weighting[3:-1]
        LWA = _calculateA_weighted(lst)
        ax.semilogx(Octave_bands[3:-1], lst,color="dimgray", label="Sound power level: L_W")
        ax.semilogx(Octave_bands[3:-1], a_weighted, color="forestgreen",label="A-weighted Sound power level: L_W,A")
        title = "Sound power level with and without A-weighting\n L_WA = {}".format(round(LWA,1))

    else:
        for i, val in enumerate(lst):

            #if (plot_B==False):
            #    ax.semilogx(Octave_bands[3:-1], val - B, label=" Delta Lpi: Position {0}".format(i + 1))
            #else:
            ax.semilogx(Octave_bands[3:-1], val, label=" Position {0}".format(i + 1))

    ax.grid(which="major")
    ax.grid(which="minor", linestyle=":")
    ax.set_xlabel("Frequency [Hz]")
    ax.set_ylabel("Amplitude [dB]")
    ax.set_title(title)
    ax.set_xticks(Octave_bands[3:-1])
    ax.set_xticklabels(x_ticks_octaveband[3:-1])

    #ax.semilogx(Octave_bands[3:-1], B, label=" Delta Lpi: Position {0}".format(i + 1))
    if DeltaLf :
        plt.axline((125,7),(8000,7),linestyle="--", linewidth=0.8, color="r", label="Seperation line for Grade 2&3")
        plt.legend(loc="upper right")
    else : plt.legend(loc="lower right")

    plt.show()


def _plotTSRSSB_Semilogx(ref, test, B, title=" "):
    fig, ax = plt.subplots()

    for i, val in enumerate(ref):
        # if (plot_B==False):
        #    ax.semilogx(Octave_bands[3:-1], val - B, label=" Delta Lpi: Position {0}".format(i + 1))
        # else:
        ax.semilogx(Octave_bands[3:-1], val - B,color="forestgreen")#, label="RSS Position {0}".format(i + 1))

    for i, val in enumerate(test):
        # if (plot_B==False):
        #    ax.semilogx(Octave_bands[3:-1], val - B, label=" Delta Lpi: Position {0}".format(i + 1))
        # else:
        ax.semilogx(Octave_bands[3:-1], val - B, color="dimgray")#, label="TS Position {0}".format(i + 1))

    ax.grid(which="major")
    ax.grid(which="minor", linestyle=":")
    ax.set_xlabel("Frequency [Hz]")
    ax.set_ylabel("Amplitude [dB]")
    ax.set_title(title)
    ax.set_xticks(Octave_bands[3:-1])
    ax.set_xticklabels(x_ticks_octaveband[3:-1])
    #ax.semilogx(Octave_bands[3:-1], B,color="blue")
    plt.axline((125, 15), (8000, 15), linestyle="--", linewidth=0.8, color="r", label="Seperation line for Background noise correction")
    plt.legend()
    plt.show()

def _calculateA_weighted(LW):
    sum = 0
    for i, val in enumerate(LW):
        avekt = [A_weighting[3+i]]
        sum += 10**(0.1 * (val + A_weighting[3+i]))
    LWA = 10*np.log10(sum)
    print(LWA)
    return LWA

def _ReferenceArray_Lpi(array, plot):
    out = []
    for i in Reference_source_M1 : out.append(array[i])
    if plot : _plotSemilogx(out)
    return out

def _Method2arr(array, plot):
    out = []
    for i in Method_2 : out.append(array[i])
    if plot : _plotSemilogx(out)
    return out

def _TestArray_Lpi(array,plot):
    out = []
    for i in Test_source_M1 : out.append(array[i])
    if plot : _plotSemilogx(out)
    return out

def _checkCorrected(array, Lpiarray):
    for i in range(array.shape[0]):
        print("#######  Position {}  ########".format(i))
        for y in range(array.shape[1]):
            print("Octave band {0} : Difference: {1}".format(Octave_bands2[y], (round(array[i][y],1) - round(Lpiarray[i][y],1))))


def _Background_Lpi(array):
    out = []
    log_mean = []
    for i in Background_noise_M1 : out.append(array[i])
    Back_avg_mean = np.transpose(np.array(out))
    for i in Back_avg_mean : log_mean.append(_calculate_log_mean(i))
    return out, log_mean


def _calculateDeltaLf(arr, type):
    clean_arr = arr*0
    for i, val in enumerate(arr):
        for y, val2 in enumerate(val):
            if type == "RSS":
                clean_arr[i][y] = val2 - L_W_RSS[y] + 11 + 20*np.log10(r_rss[i] / 1)
            if type == "ST":
                clean_arr[i][y] = val2 - L_W_RSS[y] + 11 + 20 * np.log10(r_ts[i] / 1)
    _plotSemilogx(clean_arr,DeltaLf=True)

def _soundPowerLevels(ST, RSS):
    ST = np.transpose(ST)
    RSS = np.transpose(RSS)
    LW = []
    for i in range(ST.shape[0]):
        temp = 0
        for y in range(ST.shape[1]):
            temp += 10**(0.1 * (ST[i][y] - RSS[i][y]))
        LW.append(L_W_RSS[i] + 10*np.log10(0.2 * temp))
    _plotSemilogx(LW)



noise, data = _LeqArray("Trykk_Lab1.csv")

back, log_mean = _Background_Lpi(data)

ref = _ReferenceArray_Lpi(data, plot=True)
test = _TestArray_Lpi(data,plot=True)
LpiST = _calculateLpiST(test, log_mean)
LpiRSS = _calculateLpiRSS(ref, log_mean)
test = np.array(test)
ref = np.array(ref)
LpiRSS = np.array(LpiRSS)
_soundPowerLevels(test, ref)
_checkCorrected(test, LpiST)

_calculateDeltaLf(ref, "RSS")
_plotTSRSSB_Semilogx(ref,test,log_mean)
_createLpiB(noise)



######### Method 2 #########
def _surfaceArea(lst):
    x = lst[0]
    y = lst[1]
    z = lst[2]
    Sv = x*y + 2*x*z + 2*y*z
    print (Sv)
    return Sv
def _K2A(alpha):
    Sv = _surfaceArea(room_size)
    S = _surfaceArea(M2_box)
    K2A = 10*np.log10(1 + (4*S / (alpha * Sv)))
    print("K2A = ", K2A)
    return K2A

def _LpiA(LpA):
    arr = np.transpose(np.array(LpA))
    Lpa = []
    for i, val in enumerate(arr):
        temp = 0
        for y in val:
            temp += 10**(0.1 * y)

        Lpa.append(10*np.log10(0.2 * temp))

    return Lpa


def _plotDeltaLA(LpA, LpAB, title=" "):
    fig, ax = plt.subplots()
    LpA = np.array(LpA)
    LpAB = np.array(LpAB)
    plot = LpA - LpAB
    ax.semilogx(Octave_bands[3:-1],plot)
    ax.grid(which="major")
    ax.grid(which="minor", linestyle=":")
    ax.set_xlabel("Frequency [Hz]")
    ax.set_ylabel("Amplitude [dB]")
    ax.set_title(title)
    ax.set_xticks(Octave_bands[3:-1])
    ax.set_xticklabels(x_ticks_octaveband[3:-1])
    plt.axline((125, 10), (8000, 10), linestyle="--", linewidth=0.8, color="r", label="Seperation line for Background noise correction")
    plt.legend()
    plt.show()

def _AvgLpa(M2_arr):
    out = []
    for i in M2_arr:
        LpA = np.array(i) + np.array(A_weighting)
        temp = 0
        for y in LpA:
            temp += 10 ** (y / 10)
        out.append(10*np.log10(temp))
        #out.append(_calculate_log_mean(LpA))
    temp = 0
    for i in out:
        temp += 10**(0.1 * i)

    return 10 * np.log10(0.2 * temp)

def _LWAM2(LPA, K1, K2, S, S0):
    return LPA - K1 - K2 + 10*np.log10(S / S0)


_surfaceArea(room_size)
_K2A(0.05)
log_mean = np.array(log_mean)
print(log_mean,"-----------------------------------------------------")
A_weighting = np.array(A_weighting[3:-1])
LpiBA = log_mean + A_weighting
met2 = np.array(_Method2arr(data, plot=True))
LpiA = np.array(_LpiA(met2))
#_plotDeltaLA(LpiA, LpiBA)
print("#-#-#-#",_AvgLpa(met2))
K1 = 0
K2 = _K2A(0.05)
S0 = 1
S = _surfaceArea(M2_box)
print(_LWAM2(_AvgLpa(met2),K1,K2,S,S0))




""" 
def _plot_DeltaLf(array):

    fig, ax = plt.subplots()
    for i, val in enumerate(Reference_source_M1) :
        Delta_Lf = []
        for y,val2 in enumerate(L_W_RSS) :
            temp = array[i][18+y] - val2 + 11 + (20 * np.log10(r_rss[i] / 1))
            Delta_Lf.append(temp)
        ax.semilogx(Octave_bands[3:-1], Delta_Lf, label=" Position {0}".format(i))
        ax.grid(which="major")
        ax.grid(which="minor", linestyle=":")
        ax.set_xlabel("Frequency [Hz]")
        ax.set_ylabel("Amplitude [dB]")
        # ax.set_title("Microphone positions 1-5 - test {0}".format(Test_type[i]))
        ax.set_title(" ")
        ax.set_xticks(Octave_bands[3:-1])
        ax.set_xticklabels(x_ticks_octaveband[3:-1])
        plt.legend(loc="lower right")
    plt.show()
    return Delta_Lf

def _Test_Types(array, M_type):
    temp = []

    for i in array:
        if i == 0: temp.append("Background")
        if i == 1: temp.append("Reference")
        if i == 2: temp.append("Test")
        if i == 15: temp.append("M2_Front")
        if i == 16: temp.append("M2_Right")
        if i == 17: temp.append("M2_Left")
        if i == 18: temp.append("M2_Back")
        if i == 19: temp.append("M2_Top")

    title = _create_title_M1and2(temp, M_type)
    return temp, title



def _create_plot_array(back=False, test=False, ref=False, M2 = False):
    out = []
    if(back):
        for i in Background_noise_M1: out.append(i)
    if(test):
        for i in Test_source_M1: out.append(i)
    if(ref):
        for i in Reference_source_M1: out.append(i)
    if(M2):
        for i in Method_2: out.append(i)
    return out


def _create_title_M1and2(lst, M_type):
    if (M_type==0):
        title = str("Method 1 Mic. pos 1-5 - Test types: " + " & ".join(lst))
    if (M_type == 1):
        title = str("Method 2 Mic. pos:" + "/".join(lst))
    if (M_type == 2):
        title = str("Method 1 & 2 - Test types M1: " + " & ".join(lst[0:1]) + str(" & Test pos. M2: " + " - ".join(lst[2:])))
    return title


def _create_array(file):
    df = pd.read_csv(file, sep=";")

    array = df.to_numpy()
    Data_array = array[:,4:].astype(np.float)
    print(df.dtypes)

    plot_list = _create_plot_array(back, test, ref, M2)
    #_plot_section(plot_list,Data_array)
    _plot_DeltaLf(Data_array)




def _plot_section(list, array):

    fig, ax = plt.subplots()
    for i in list:
        k = 0
        temp = array[i, 15:26] + A_weighting
        print(np.average(temp))
        if(i <15) :  ax.semilogx(Octave_bands,temp, label="Mic. position {0} - {1} Measurement".format(Positions[i],Test_type[i]))
        else :
            ax.semilogx(Octave_bands,temp, label="Mic. position {0}".format(Sides[k]))
            k += 1




    lst, title = _Test_Types(list, M)

    ax.grid(which="major")
    ax.grid(which="minor", linestyle=":")
    ax.set_xlabel("Frequency [Hz]")
    ax.set_ylabel("Amplitude [dB]")
    #ax.set_title("Microphone positions 1-5 - test {0}".format(Test_type[i]))
    ax.set_title(title)
    ax.set_xticks(Octave_bands)
    ax.set_xticklabels(x_ticks_octaveband)
    plt.legend(loc="lower right")
    plt.show()


if __name__ == '__main__':


    _create_array("Trykk_Lab1.csv")
    
    """