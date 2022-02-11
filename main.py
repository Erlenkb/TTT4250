import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


##Global
x_ticks_octaveband = ["16","31.5","63","125", "250", "500", "1k", "2k", "4k", "8k", "16k"]
A_weighting = [-56.7, -39.4, -26.2, -16.1, -8.6, -3.2, 0, 1.2, 1, -1.1, -4]
Octave_bands = [16,31.5,63,125,250,500,1000,2000,4000,8000,16000]
po = 20*(10**(-5))

##Metode 1
Header_list = ["Name","Start", "Time","Duration","Unit","LAeq",	"LAFmax","LAFmin","LAE","LApeak","LCeq","LCFmax","LCFmin","LCE","LCpeak","LZeq","LZFmax","LZFmin","LZE","LZpeak","Lfeq 16 Hz","Lfeq 31.5 Hz","Lfeq 63 Hz", "Lfeq 125 Hz", "Lfeq 250 Hz", "Lfeq 500 Hz", "Lfeq 1 kHz", "Lfeq 2 kHz", "Lfeq 4 kHz", "Lfeq 8 kHz", "Lfeq 16 kHz", "LfFmax 16 Hz", "LfFmax 31.5 Hz", "LfFmax 63 Hz", "LfFmax 125 Hz", "LfFmax 250 Hz", "LfFmax 500 Hz", "LfFmax 1 kHz", "LfFmax 2 kHz", "LfFmax 4 kHz", "LfFmax 8 kHz", "LfFmax 16 kHz", "LfFmin 16 Hz", "LfFmin 31.5 Hz", "LfFmin 63 Hz", "LfFmin 125 Hz", "LfFmin 250 Hz", "LfFmin 500 Hz", "LfFmin 1 kHz", "LfFmin 2 kHz", "LfFmin 4 kHz", "LfFmin 8 kHz", "LfFmin 16 kHz", "LfE 16 Hz", "LfE 31.5 Hz", "LfE 63 Hz", "LfE 125 Hz", "LfE 250 Hz", "LfE 500 Hz", "LfE 1 kHz", "LfE 2 kHz", "LfE 4 kHz", "LfE 8 kHz", "LfE 16 kHz"]
Positions = ["1","1","1","2","2","2","3","3","3","4","4","4","5","5","5",]
Test_type = ["Background","Reference","Test","Test","Reference","Background","Background","Test","Reference","Background","Test","Reference","Background","Test","Reference"]
L_W_RSS = [79.8, 81, 80.9, 84.9, 85.1, 82.7,  79.2] # 125 - 8000Hz
r_rss = [1.524, 2.48, 2.899, 3.469, 2.22]

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
    Data_Arrray = array[:,18:25].astype(np.float)
    noise = []
    for i in Background_noise_M1 : noise.append(array[i,Noise_Val])
    return noise, Data_Arrray

def _getPressure(val1, val2):
    return 10**(val1 / 10), 10**(val2 / 10)

def _calculate_log_mean(lst):
    avg_db = 0
    for i, val in enumerate(lst):
        if ( i < len(lst)-1):
            if ( i == 0): val1 = val
            else : val1 = avg_db
            val2 = lst[i+1]
            x,y = _getPressure(val1, val2)
            avg = 0.5 * (y + x)
            #nevner = val2 - val1
            #avg = ((y-x)) / (val2 - val1)
            avg_db = round(10*np.log10(avg),1)
            print("value : ", avg_db)
    return avg_db

def _createLpiB(noise):
    LpiB = _calculate_log_mean(noise)
    print("########",LpiB)
    return LpiB

def _calculateLpi(Ref,LpiB):
    for i in


def _ReferenceArray_Lpi(array):
    out = []
    for i in Reference_source_M1 : out.append(array[i])
    return out

def _TestArray_Lpi(array):
    out = []
    for i in Test_source_M1 : out.append(array[i])
    return out




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