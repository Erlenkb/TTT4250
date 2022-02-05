import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

Header_list = ["Name","Start", "Time","Duration","Unit","LAeq",	"LAFmax","LAFmin","LAE","LApeak","LCeq","LCFmax","LCFmin","LCE","LCpeak","LZeq","LZFmax","LZFmin","LZE","LZpeak","Lfeq 16 Hz","Lfeq 31.5 Hz","Lfeq 63 Hz", "Lfeq 125 Hz", "Lfeq 250 Hz", "Lfeq 500 Hz", "Lfeq 1 kHz", "Lfeq 2 kHz", "Lfeq 4 kHz", "Lfeq 8 kHz", "Lfeq 16 kHz", "LfFmax 16 Hz", "LfFmax 31.5 Hz", "LfFmax 63 Hz", "LfFmax 125 Hz", "LfFmax 250 Hz", "LfFmax 500 Hz", "LfFmax 1 kHz", "LfFmax 2 kHz", "LfFmax 4 kHz", "LfFmax 8 kHz", "LfFmax 16 kHz", "LfFmin 16 Hz", "LfFmin 31.5 Hz", "LfFmin 63 Hz", "LfFmin 125 Hz", "LfFmin 250 Hz", "LfFmin 500 Hz", "LfFmin 1 kHz", "LfFmin 2 kHz", "LfFmin 4 kHz", "LfFmin 8 kHz", "LfFmin 16 kHz", "LfE 16 Hz", "LfE 31.5 Hz", "LfE 63 Hz", "LfE 125 Hz", "LfE 250 Hz", "LfE 500 Hz", "LfE 1 kHz", "LfE 2 kHz", "LfE 4 kHz", "LfE 8 kHz", "LfE 16 kHz"]






def print_hi(file):
    df  = pd.read_csv(file, sep=";")
    Name = Header_list[0]
    #print(df.columns[20:])
    #print(Header_list.index("Name"))
    matrix = df.get(Header_list[20:])
    #plt.plot(matrix[1])
    print(df.dtypes)


if __name__ == '__main__':

    print_hi("Trykk_Lab1.csv")