import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

octave_band = [125, 250, 500, 1000, 2000, 4000, 8000, 16000]
A_weighting = np.array([-16.1, -8.6, -3.2, 0, 1.2, 1, -1.1, -4])
x_ticks_octaveband = ["125", "250", "500", "1k", "2k", "4k", "8k", "16k"]
p0 = 20 * 10 ** (-6)
LW_RSS_A_tot = 90.5
r = np.array([1.524, 2.480, 2.899, 3.469, 2.220])
LW_RSS_short = np.array([79.8, 81.0, 80.9, 84.9, 85.1, 82.7, 79.2])
A_weighting_modded = A_weighting[:-1]
mic_pos = 5

MEASUREMENT = {
    "LFEQ": 0,
    "LFMAX": 1,
    "LFMIN": 2,
    "LFE": 3
}

unmodded_file_ref = "Trykk_Lab1.csv"


# = "intensitet_lab1.csv"


def read_csv(filename):
    return np.genfromtxt(filename, skip_header=1, delimiter=';')


# Array of type:  [ROWS, OCTAVEBANDS]
def plått(array, title, name_of_file, use_A_Weight=True, short=False, ) -> object:
    fig, ax = plt.subplots()
    for i in range(array.shape[0]):
        if not short:
            ax.semilogx(octave_band, array[i] + (A_weighting * np.array(use_A_Weight).astype(int)),
                        label=f"Mic pos {i + 1}")
        else:
            ax.semilogx(octave_band[:-1], array[i] + (A_weighting * np.array(use_A_Weight).astype(int))[:-1],
                        label=f"Mic pos {i + 1}")
    # plot magic
    ax.grid(which="major")
    ax.grid(which="minor", linestyle=":")
    ax.set_xlabel("Frequency [Hz]")
    ax.set_ylabel("Amplitude [dB]")
    ax.set_title(title)
    if not short:
        ax.set_xticks(octave_band)
        ax.set_xticklabels(x_ticks_octaveband)
    else:
        ax.set_xticks(octave_band[:-1])
        ax.set_xticklabels(x_ticks_octaveband[:-1])

    #plt.legend(loc="lower right")
    plt.savefig(name_of_file)
    plt.show()


def background_noise_correction(L_marked_pi):
    L_pi = 10 * np.log10(10 ** (L_marked_pi / 10) - 10 ** (L_marked_pi / 10))


def db_to_pressure(measurements):
    return 10 ** (measurements /10)


def pressure_to_db(measurements):
    return 10 * np.log10(measurements)


# Reading the files
data = read_csv(unmodded_file_ref)[:-1, 4:]  # All rows minus the last, header is fucked anyway, fuck the first 4 colums
print("data shape", data.shape)

bg_noise = data[[0, 5, 6, 9, 12], :]
print("bg noise shape", bg_noise.shape)

ref_noise = data[[1, 4, 8, 11, 14], :]
print("ref noise shape", ref_noise.shape)

test_noise = data[[2, 3, 7, 10, 13], :]
print("test", test_noise.shape)

method_2_data = data[[15, 16, 17, 18, 19]]
print('method 2 data', method_2_data.shape)
#
# data_method3 = pd.read_csv(filelist, sep=";")
# data_method3 = np.array(data_method3)
# print('data 3', data_method3.shape)
# print('data3', data_method3)

# Trash the first 15 columns as they are not relevant for the octavebands
# Split into microphone positions, measurement and octavebands
reference_splitted = ref_noise[:, 15:].reshape(-1, 4, 11)[:, :,3:]  # The three first octave bands are invalid due to measurement equipment limitation
background_splitted = bg_noise[:, 15:].reshape(-1, 4, 11)[:, :, 3:]
test_splitted = test_noise[:, 15:].reshape(-1, 4, 11)[:, :, 3:]
method_2_splitted = method_2_data[:, 15:].reshape(-1, 4, 11)[:, :, 3:]
# method_3_splitted = data_method3[10:,[0,2,4,5]]

# print('met3 shape', method_3_splitted.shape)
# print('met3 ', method_3_splitted)


print("Microphone positions, measurements, octavebands", reference_splitted.shape)
to_plot_ref = reference_splitted[:, MEASUREMENT["LFEQ"], :]
to_plot_back = background_splitted[:, MEASUREMENT["LFEQ"], :]
to_plot_test = test_splitted[:, MEASUREMENT["LFEQ"], :]
to_plot_method2 = method_2_splitted[:, MEASUREMENT["LFEQ"], :]

# Calculate average background noise per octaveband
background_pressure = db_to_pressure(to_plot_back)
print("PRessure_vec shape", background_pressure.shape)

pres_avg = np.average(background_pressure, axis=0)

# From pressure to dB
average_background = pressure_to_db(pres_avg)

#################################


# plått([to_plot_ref, to_plot_test], "Reference sound source", name_of_file='ref_method1_plt.pdf')
# plått(to_plot_test, 'Test sound source', name_of_file='test_method1_plt.pdf')

# Calculating delta Lpi,RSS and delta Lpi,TS
delta_ref = to_plot_ref - average_background
delta_test = to_plot_test - average_background

# plått(delta_ref, 'Delta Lpi RSS', name_of_file='deltapi_ref_method1_plt.pdf')
# plått(delta_test, 'Delta Lpi TS', name_of_file='deltapi_test_method1_plt.pdf')

# Calculating delta Lf
print('plot ref', to_plot_ref.shape)
print('lw_rss', LW_RSS_short.shape)

delta_lf_short = to_plot_ref[:, :-1] - LW_RSS_short + 11 + 20 * np.log10(r.reshape(1, -1).transpose())

# plått(delta_lf_short, 'Delta LF', name_of_file='deltalf_method1_plt.pdf', short=True)

# Calculation of Sound Power Levels
sum_sound_pressure_short = db_to_pressure(to_plot_test[:, :-1] - to_plot_ref[:, :-1])
print('test unmodded', to_plot_test)
print('test', to_plot_test[:, :-1])
print('test pressure', db_to_pressure(to_plot_test[:,:-1]))

print('ref unmodded', to_plot_ref)
print('ref', to_plot_ref[:, :-1])
print('ref pressure', db_to_pressure(to_plot_ref[:,:-1]))



print('sum sound pressure', sum_sound_pressure_short)
# import sys
# sys.exit(1)

print('sum sound pressure', sum_sound_pressure_short)
print(sum_sound_pressure_short.shape)

sound_pressure_avg = pressure_to_db(np.average(db_to_pressure(sum_sound_pressure_short)))
print(sound_pressure_avg)

L_W_short = LW_RSS_short + 10 * np.log10((1 / mic_pos) * sound_pressure_avg)
print('lw', L_W_short)
# plått(np.array([L_W_short]), title='Sound Power Levels, L_W', name_of_file='lw_met1.pdf', short=True)

# Calculating A-weighted sound power
# pressure_vec_short = db_to_pressure(L_W_short + A_weighting[:-1])
# print('pressure ve c short',pressure_vec_short)
# total_pressure = np.sum(pressure_vec_short, axis=0)
# print('total pressure',total_pressure)

L_W_A = pressure_to_db(np.sum(db_to_pressure(L_W_short +A_weighting[-1])))
print('L_W_A', L_W_A)



######################################################
# Method 2
######################################################

# Environment Correction

# Equivalent absorption area
alpha = 0.05
Surface = 2 * (6.042 * 5.174) + 2 * (5.174 * 8.501) + 2 * (8.501 * 6.042)
print('Sv', Surface)
Absorption_area = alpha * Surface
print('abs area', Absorption_area)
meas_length = 0.465
meas_width = 0.3
meas_height = 0.25
meas_surface = 2 * (meas_width * meas_height) + 1 * (meas_width * meas_length) + 2 * (meas_length * meas_height)
print('meas surface', meas_surface)
K_2A = 10 * np.log10(1 + 4 * (meas_surface / Absorption_area))
print('KA2', K_2A)
#K_2A = 0.045

# Calculating averaged A-weighted background noise

weighted_background = average_background + A_weighting
# plått(np.array([weighted_background]), title ='A-weighted background noise', name_of_file ='background_method2_plt.pdf')

# Calculating average sound pressure levels per octave band
# background_pressure = db_to_pressure(to_plot_back)
# pres_avg = np.average(background_pressure, axis=0)

# From pressure to dB
# average_background = pressure_to_db(pres_avg)
meas_pressure = db_to_pressure(to_plot_method2)
print('toplotmet2', to_plot_method2)
pres_avg_method2 = np.average(meas_pressure, axis = 0)
avg_spl_metod2 = pressure_to_db(pres_avg_method2)

# avg_spl_metod2 = pressure_to_db(np.average(db_to_pressure(to_plot_method2, axis=0)))


#averaged spl
# plått(np.array([avg_spl_metod2]), title='Averaged A-weighted SPL', name_of_file='avg_spl_met2.pdf')
#Sound pressure level
# plått(to_plot_method2, title='Sound pressure level', name_of_file='spl_met2.pdf')

# Calculate background noise correction
delta_LA = avg_spl_metod2 - average_background
print('delta la', delta_LA)
# plått(np.array([delta_LA]), title='Delta LA', name_of_file='deltala_method2.pdf')

# Calculate A-weighted Sound Power Level
K_1A = 0
LW_2 = avg_spl_metod2 - K_1A - K_2A + 10 * np.log10(meas_surface)
LWA_2 = avg_spl_metod2 + A_weighting[-1] - K_1A - K_2A + 10 * np.log10(meas_surface)
LWA_2_tot = pressure_to_db(np.sum(db_to_pressure(LWA_2)))
LW_TOT = pressure_to_db(np.sum(db_to_pressure(LW_2)))
# plått(np.array([LWA_2, LW_2], dtype=object), title='Sound Power Level L_W,A', name_of_file='lwa_method2_zweight.pdf', use_A_Weight=False)
#plått(np.array([LWA_2]), title='Sound Power Level L_W,A', name_of_file='lwa_method2_aweight.pdf', )

print('LWA2tot', LWA_2_tot)
print('LWtot', LW_TOT)

