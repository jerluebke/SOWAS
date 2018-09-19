#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This script creates the visualisation of the results of 2018s SOWAS Project at
Ruhr-University
Considered is a chain of evenly spaced and evenly shaped dominoes

Two plots are drawn:
    1. Development of transversal velocity for spacing=3cm along the x axis
    (positions of dominoes in the chain)
    2. Asymptotical velocities for different spacings

Each plot compares experimental data taken during the project and theoretical
data computed by associated programs


author: Jeremiah Lübke
date: 06.2018
"""
 
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import dominoes
import v_vs_x

mpl.rcParams["font.size"] = 22
mpl.rcParams["font.family"] = "sans-serif"
mpl.rcParams["font.sans-serif"] = "Calibri"
mpl.rcParams["xtick.major.size"] = 6
mpl.rcParams["xtick.major.width"] = 1.8
mpl.rcParams["ytick.major.size"] = 6
mpl.rcParams["ytick.major.width"] = 1.8
mpl.rcParams["grid.linewidth"] = 1.2
mpl.rcParams["lines.linewidth"] = 2


EXP_DATA_ALL    = "./velocities_by_x.dat"
EXP_DATA_3CM    = "./experimental_data_avg.dat"
FIGSIZE         = (16, 8)   #  (12, 8)
ERRORBAR_PROPS  = dict(ecolor="black", capsize=5, marker="o",
                       markersize=8, color="red",
                       elinewidth=1.8, capthick=1.2,
                       linestyle="None")
DPI             = 300
DOMINO_PROPS    = dict(height=4.2, width=0.6, energy_loss=0.9)
PIECES          = 30
INITIAL_VEL     = 0.8
LABEL_EXP       = "Experiment"
LABEL_TH        = "gefittete Theorie"


def main_compare(save=False):
    # init calculations and get data
    v_vs_x.init(**DOMINO_PROPS, spacing=2.4, length=PIECES, initial=INITIAL_VEL)
    dominoes.init(**DOMINO_PROPS)
    pos         = np.arange(0, 90, 3)
    vel_3cm_exp = np.fromfile(EXP_DATA_ALL).reshape(34, 3)[:-4]
    vel_3cm_th  = v_vs_x.velocities()
    exp_data    = np.fromfile(EXP_DATA_3CM).reshape(6, 3)
    spacings    = np.linspace(1.5, 4)
    vel_all     = np.array(list(map(lambda x: dominoes.velocity(x),
                                    spacings-0.6)))
    vel_as      = dominoes.velocity(2.4)

    # plotting
    fig, ax = plt.subplots(ncols=2, figsize=FIGSIZE)

    # add horizontal line indicating the asymptotical velocity
    ax[0].plot((0, 70), 2*(vel_as,), linestyle=(5, (5, 5)), color="grey")
    # progression of velocity for 3 cm spacing
    ax[0].errorbar(pos, vel_3cm_exp.mean(axis=1), vel_3cm_exp.std(axis=1),
                   **ERRORBAR_PROPS, label=LABEL_EXP)
    ax[0].plot(pos, vel_3cm_th,
               label=LABEL_TH)
    # adjustments
    ax[0].set_xlim(1.5, 61.5)

    # plot velocity vs spacing
    ax[1].errorbar(exp_data[::,0], exp_data[::,1], exp_data[::,2],
                   **ERRORBAR_PROPS, label=LABEL_EXP)
    ax[1].plot(spacings, vel_all, label=LABEL_TH)

    # text-related
    ax[0].legend(loc="lower left", numpoints=1)
    ax[1].legend(loc="lower left", numpoints=1)
    ax[0].set(xlabel="x [$10^{-2}$ m]",
              ylabel="v [$\\frac{m}{s}$]",
              #  title="Geschwindigkeitsverlauf für d = 3 cm")
             )
    ax[1].set(xlabel="d [$10^{-2}$ m]",
              ylabel="v [$\\frac{m}{s}$]",
              #  title="$v_{as}$ verschiedener Abstände")
             )

    if save:
        plt.tight_layout()
        plt.savefig("%s.png" % input("name: "), dpi=DPI)
