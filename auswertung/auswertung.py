#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt
import dominoes
import v_vs_x


EXP_DATA_ALL    = "./velocities_by_x.dat"
EXP_DATA_3CM    = "./experimental_data_avg.dat"
FIGSIZE         = (32, 16)   #  (12, 8)
ERRORBAR_PROPS  = dict(ecolor="black", capsize=5, marker="o",
                       markersize=6, color="red",
                       linestyle="None")
DPI             = 300
DOMINO_PROPS    = dict(height=4.2, width=0.6, energy_loss=0.9)
PIECES          = 30
INITIAL_VEL     = 0.8


def main_compare():
    # init calculations
    v_vs_x.init(**DOMINO_PROPS, length=PIECES, initial=INITIAL_VEL)
    dominoes.init(**DOMINO_PROPS)
    pos         = np.arange(0, 90, 3)
    vel_3cm_exp = np.fromfile(EXP_DATA_ALL).reshape(34, 3)[:-4]
    vel_3cm_th  = v_vs_x.velocities()
    exp_data    = np.fromfile(EXP_DATA_3CM).reshape(6, 3)
    spacings    = np.linspace(1.5, 4)
    vel_all     = np.array(list(map(lambda x: dominoes.velocity(x),
                                    spacings-0.6)))

    # plotting
    fig, ax = plt.subplots(ncols=2, figsize=FIGSIZE)

    # progression of velocity for 3 cm spacing
    ax[0].errorbar(pos, vel_3cm_exp.mean(axis=1), vel_3cm_exp.std(axis=1),
                   **ERRORBAR_PROPS)
    ax[0].plot(pos, vel_3cm_th)
    # add horizontal line indicating the asymptotical velocity
    ax[0].plot((0, 70), 2*(dominoes.velocity(2.4),), "--", color="grey")

    # plot velocity vs spacing
    ax[1].errorbar(exp_data[::,0], exp_data[::,1], exp_data[::,2],
                   **ERRORBAR_PROPS)
    ax[1].plot(spacings, vel_all)

    # adjustments
    ax[0].set_xlim(1.5, 61.5)

