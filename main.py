import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

Header_list = ["Name","Start", "Time","Duration","Unit","LAeq",	"LAFmax","LAFmin","LAE","LApeak","LCeq","LCFmax","LCFmin","LCE","LCpeak","LZeq","LZFmax","LZFmin","LZE","LZpeak","Lfeq 16 Hz","Lfeq 31.5 Hz","Lfeq 63 Hz", "Lfeq 125 Hz", "Lfeq 250 Hz", "Lfeq 500 Hz", "Lfeq 1 kHz", "Lfeq 2 kHz", "Lfeq 4 kHz", "Lfeq 8 kHz", "Lfeq 16 kHz", "LfFmax 16 Hz", "LfFmax 31.5 Hz", "LfFmax 63 Hz", "LfFmax 125 Hz", "LfFmax 250 Hz", "LfFmax 500 Hz", "LfFmax 1 kHz", "LfFmax 2 kHz", "LfFmax 4 kHz", "LfFmax 8 kHz", "LfFmax 16 kHz", "LfFmin 16 Hz", "LfFmin 31.5 Hz", "LfFmin 63 Hz", "LfFmin 125 Hz", "LfFmin 250 Hz", "LfFmin 500 Hz", "LfFmin 1 kHz", "LfFmin 2 kHz", "LfFmin 4 kHz", "LfFmin 8 kHz", "LfFmin 16 kHz", "LfE 16 Hz", "LfE 31.5 Hz", "LfE 63 Hz", "LfE 125 Hz", "LfE 250 Hz", "LfE 500 Hz", "LfE 1 kHz", "LfE 2 kHz", "LfE 4 kHz", "LfE 8 kHz", "LfE 16 kHz"]
Positions = ["1","1","1","2","2","2","3","3","3","4","4","4","5","5","5",]
Test_type = ["Background","Reference","Test","Test","Reference","Background","Background","Test","Reference","Background","Test","Reference","Background","Test","Reference"]
x_ticks_octaveband = ["16","31.5","63","125", "250", "500", "1k", "2k", "4k", "8k", "16k"]




A_weighting = [-56.7, -39.4, -26.2, -16.1, -8.6, -3.2, 0, 1.2, 1, -1.1, -4]
Octave_bands = [16,31.5,63,125,250,500,1000,2000,4000,8000,16000]


##Metode 1
Background_noise_M1 = [0,5,6,9,12]
Test_source_M1 = [2,3,7,10,13]
Reference_source_M1 = [1,4,8,11,14]

#Metode 2



########################## Define what you want to plot ################


back = False
test = False
ref = True




#######################################################################






def _create_plot_array(back=False, test=False, ref=False):
    out = []
    if(back):
        for i in Background_noise_M1: out.append(i)
    if(test):
        for i in Test_source_M1: out.append(i)
    if(ref):
        for i in Reference_source_M1: out.append(i)
    return out


def _create_array(file):
    df = pd.read_csv(file, sep=";")

    array = df.to_numpy()
    Data_array = array[:,4:].astype(np.float)
    print(df.dtypes)

    plot_list = _create_plot_array(back, test, ref)
    _plot_section(plot_list,Data_array)

def _plot_section(list, array):

    fig, ax = plt.subplots()
    for i in list:
        temp = array[i, 15:26] + A_weighting
        print(np.average(temp))
        ax.semilogx(Octave_bands,temp, label="Mic. position {0} - {1} Measurement".format(Positions[i],Test_type[i]))

    ax.grid(which="major")
    ax.grid(which="minor", linestyle=":")
    ax.set_xlabel("Frequency [Hz]")
    ax.set_ylabel("Amplitude [dB]")
    ax.set_title("Microphone positions 1-5 - test {0}".format(Test_type[i]))
    ax.set_xticks(Octave_bands)
    ax.set_xticklabels(x_ticks_octaveband)
    plt.legend(loc="lower right")
    plt.show()


if __name__ == '__main__':


    _create_array("Trykk_Lab1.csv")