#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import numpy as np
import matplotlib.pyplot as plt
import dominoes


#################
#   GLOBALS     #
#################

# general settings
DATA_DIR        = "./text"
FILE_TYPE       = ".txt"
FIRST_ELEMS     = 4
LAST_ELEMS      = 1
FIGSIZE         = (12, 8)
ERRORBAR_PROPS  = dict(ecolor="black", capsize=5, marker="o",
                       markersize=6, color="red",
                       linestyle="None")
DPI             = 300

# spacings and friction
LAMBDAS = np.array([
    1.5,
    2.0,
    2.5,
    3.0,
    3.5,
    4.0,
])
MU = [
    0.2,
    0.4,
]

# saving figures here
FIGURE  = []


#################
#   FUNCTIONS   #
#################

def get_data()->np.ndarray:
    return np.array([get_content(file) for file in os.listdir(DATA_DIR)
                     if file.endswith(FILE_TYPE)])

def get_content(file:str)->np.ndarray:
    with open(os.path.join(DATA_DIR, file), 'r') as f:
        lines = f.readlines()
    return np.array(lines[FIRST_ELEMS:], dtype=np.float64)

def calc_mean_and_std(data:np.ndarray)->np.ndarray:
    return np.array([
        (lambda arr: [np.mean(arr), np.std(arr)])(np.abs(elem[:-1] - elem[1:]))
        for elem in data
    ])

def make_plot(xdata, ydata, yerr)->list:
    fig, ax = plt.subplots(figsize=FIGSIZE)
    ax.errorbar(xdata, ydata, yerr,
                label="Experimentelle Daten",
                **ERRORBAR_PROPS)
    return [fig, ax]


def main_read_data():

    print("The Raw Data Files for this script were removed\n"\
          "For a working version with compatible data return to commit 497ffd\n"\
          "Terminating...\n")
    return -1

    global FIGURE

    # prepare data
    raw_data = get_data()*10
    time_mean, time_err = calc_mean_and_std(raw_data).transpose()
    ydata = LAMBDAS / time_mean
    # propagation of uncertainty
    yerr = LAMBDAS * time_err / time_mean**2

    # compare with theoretical intrinsic transversal
    FIGURE.append(make_plot(LAMBDAS, ydata, yerr)[0])

    dominoes.WITH_FRICTION = False
    dominoes.main()
    dominoes.WITH_FRICTION = True
    for mu in MU:
        dominoes.MU = mu
        dominoes.main()

    ax_01 = FIGURE[0].get_axes()[0]
    ax_01.set(
        title="Vergleich: Experimentelle und Theoretische Daten",
        xlabel="Abstand in m",
        ylabel="V in m/s"
    )
    plt.legend()

    return 0
