# -*- coding: utf-8 -*-

import sys
sys.path.append("..")
import os
import numpy as np
import matplotlib.pyplot as plt
import DominoChain as dc
import dominoes


#################
#   GLOBALS     #
#################

# general settings
DATA_DIR        = "./messreihe02/text"
FILE_TYPE       = ".txt"
FIRST_ELEMS     = 4
LAST_ELEMS      = 1
FIGSIZE         = (12, 8)
ERRORBAR_PROPS  = dict(ecolor="black", capsize=6, marker="o", linestyle="None")
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
LAMBDAS_LINSPACE = np.linspace(1.5, 4)
MU = [
    0.2,
    #  0.3,
    #  0.4,
    #  0.5,
    #  0.6,
    #  0.7
]

# saving figures here
FIGURE  = []

# theoretical utility
DOMINO_CHAIN = dc.PyDominoChain(dc.domino_tuple(4.2, 0.6))


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


def main():
    global FIGURE, AXIS

    # prepare data
    raw_data = get_data()*10
    time_mean, time_err = calc_mean_and_std(raw_data).transpose()
    ydata = LAMBDAS / time_mean
    yerr = LAMBDAS * time_err / time_mean**2

    # compare with theoretical intrinsic transversal
    FIGURE.append(make_plot(LAMBDAS, ydata, yerr)[0])
    #  ax_1 = FIGURE[0].get_axes()[0]
    #  [ax_1.plot(LAMBDAS_LINSPACE, (lambda x: DOMINO_CHAIN.intrinsic_velocities(
    #      x-0.3, mu)[1])(LAMBDAS_LINSPACE), label='$\mu$ = {:.1f}'.format(mu)) for mu in MU]

    dominoes.main()
    dominoes.WITH_FRICTION = True
    dominoes.main()

    #  for fig in FIGURE:
    #      fig.legend()
    #      fig.savefig("%d.png" % fig.number, dpi=DPI)

    ax_01 = FIGURE[0].get_axes()[0]
    ax_01.set(
        title="Vergleich: Experimentelle und Theoretische Daten",
        xlabel="Abstand in m",
        ylabel="V in m/s"
    )

    return 0


if __name__ == "__main__":
    main()
