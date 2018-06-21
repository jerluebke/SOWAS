#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Part of the SOWAS Project 2018 at Ruhr-Universtiy considering a chain of
dominoes

This script computes the theoretical asymptotical velocity for a fixed
spacing

From documenting each function was disregarded since this implementation is
a direct translation of the associated theory into code. A presentation of
the mathematics can be found in the dedicated .pdf-file 

The `main` function serves as an example for usage and as a test case to
quickly examine the outputted data


author: Jeremiah Lübke
date: 06.2018
"""

import numpy as np
import matplotlib.pyplot as plt


#############
#  GLOBALS  #
#############

L               = 0
H               = 0
PIECES          = 0
PHI             = 0
OMEGA_SQUARED   = 0
LAMBDA          = 0
PSI             = 0
D_THETA         = 0
ETA             = 0     # = (λ + h) / L
THETA_HAT       = 0     # = arccos(h / (h + λ))
PHI_DOT         = 0

REL_ENERGY_LOSS = 0.9
MU              = 0.101   # coefficient of friction
INT_STEPS       = 50    # number of integration steps
WITH_FRICTION   = True

G = 9.80665

FIGURE = None


###############
#  FUNCTIONS  #
###############

def velocity(lambda_value):
    update(lambda_value)
    return (LAMBDA + H) / time()

def time():
    theta_range = np.arange(0, PSI, D_THETA)
    # prevent occasional floating point error which influences the result
    if theta_range.size == INT_STEPS +1:
        theta_range = theta_range[:-1]
    # Integration of 1/theta_dot
    return np.sum(D_THETA / theta_dot(theta_range))

def theta_dot(thetas : np.ndarray) -> np.ndarray:
    k_values = np.array([k(theta) for theta in thetas])
    P_over_K_values = P_over_K(thetas)
    return PHI_DOT * np.sqrt(k_values / (k_values - 1)
                             * (1 + P_over_K_values / k_values))

def k(theta):
    return 1 + np.sum([np.prod(theta_dot_rel(j, theta)**2)
                       for j in range(PIECES)])

def theta_dot_rel(index, theta_initial) -> np.ndarray:
    thetas = np.empty(index + 1)
    thetas[0] = theta_initial
    for i in range(1, thetas.size):
        thetas[i] = np.arcsin(ETA * np.cos(thetas[i-1]) - H/L) + thetas[i-1]
    if WITH_FRICTION:
        #  a = np.cos(thetas[1:] - thetas[:-1]) - ETA * np.sin(thetas[1:]) - MU * H
        #  b = np.cos(thetas[1:] - thetas[:-1]) + MU * np.sin(thetas[1:] - thetas[:-1])
        a = np.cos(thetas[1:] - thetas[:-1]) - ETA * np.sin(thetas[:-1]) - MU * H
        b = np.cos(thetas[1:] - thetas[:-1]) + MU * np.sin(thetas[1:] - thetas[:-1])
        return a/b
    else:
        #  return 1 - ETA * np.sin(thetas[1:]) / np.cos(thetas[1:] - thetas[:-1])
        return 1 - ETA * np.sin(thetas[:-1]) / np.cos(thetas[1:] - thetas[:-1])

def P_over_K(thetas : np.ndarray) -> np.ndarray:
    return 2 * OMEGA_SQUARED * (np.cos(PHI) - np.cos(thetas - PHI)) \
            / PHI_DOT**2 - REL_ENERGY_LOSS

def phi_dot():
    k_value = k(0)
    return np.sqrt(OMEGA_SQUARED * (k_value-1) / k_value
                   * 2 * (np.cos(PHI) - np.cos(THETA_HAT - PHI)))


###########
#  SETUP  #
###########

def init(height, width, energy_loss, pieces=6):
    global L, H, PIECES, PHI, OMEGA_SQUARED, REL_ENERGY_LOSS
    L               = height
    H               = width
    PIECES          = pieces
    PHI             = np.arctan(H / L)
    OMEGA_SQUARED   = 3 * G * np.cos(PHI) / (2 * L)
    REL_ENERGY_LOSS = energy_loss

def update(spacing):
    global LAMBDA, PSI, D_THETA, ETA, THETA_HAT, PHI_DOT
    LAMBDA      = spacing
    PSI         = np.arcsin(LAMBDA / L)
    D_THETA     = PSI / INT_STEPS
    ETA         = (LAMBDA + H) / L
    THETA_HAT   = np.arccos(H / (H + LAMBDA))
    PHI_DOT     = phi_dot()

def main():
    global FIGURE
    init(4.2, 0.6, 0.9)
    spacings    = np.linspace(1.5, 4)
    velocities  = np.array(list(map(
        lambda x: velocity(x, energy_loss=0.8795), spacings-0.6)))
    if not FIGURE:
        FIGURE = plt.gcf()
    label_extension = "$\mu$ = %.1f" % MU if WITH_FRICTION else "No Friction"
    label = "Theoretischer Verlauf - %s" % label_extension
    plt.plot(spacings, velocities,
             label=label)
