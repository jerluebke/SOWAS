#!/usr/bin/env python3
# -*- coding: utf-8 -*-

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

MU              = 0.2   # coefficient of friction
INT_STEPS       = 50    # number of integration steps
WITH_FRICTION   = False

G = 9.80665

FIGURE = None
RESULT = []


###############
#  FUNCTIONS  #
###############

def velocity(lambda_value):
    update(lambda_value)
    return (LAMBDA + H) / time()

def time():
    # Integration of 1/theta_dot
    return np.sum(D_THETA / theta_dot(np.arange(0, PSI, D_THETA)))

def theta_dot(thetas : np.ndarray) -> np.ndarray:
    k_values = np.array([k(theta) for theta in thetas])
    P_over_K_value = P_over_K(thetas)
    return PHI_DOT * np.sqrt(k_values / (k_values - 1)
                             * (1 + P_over_K_value / k_values))

def k(theta):
    return 1 + np.sum([np.prod(theta_dot_rel(j, theta)**2)
                       for j in range(PIECES)])

def theta_dot_rel(index, theta_initial) -> np.ndarray:
    thetas = np.empty(index + 1)
    thetas[0] = theta_initial
    for i in range(1, thetas.size):
        thetas[i] = np.arcsin(ETA * np.cos(thetas[i-1]) - H/L) + thetas[i-1]
    return 1 - ETA * np.sin(thetas[:-1]) / np.cos(thetas[1:] - thetas[:-1])

def P_over_K(thetas : np.ndarray) -> np.ndarray:
    return 2 * OMEGA_SQUARED * (np.cos(PHI) - np.cos(thetas - PHI)) / PHI_DOT**2

def phi_dot():
    k_value = k(0)

    friction_term = 1
    if WITH_FRICTION:
        xi = L * np.cos(PSI)
        R = 1 + (xi + MU * LAMBDA) / (xi - MU * H)
        friction_term = k_value * R**2 - k_value + 1

    return np.sqrt(OMEGA_SQUARED * (k_value-1) / k_value
                   * 2 * (np.cos(PHI) - np.cos(THETA_HAT - PHI))
                   / friction_term)


###########
#  SETUP  #
###########

def init(height, width, pieces=6):
    global L, H, PIECES, PHI, OMEGA_SQUARED
    L               = height
    H               = width
    PIECES          = pieces
    PHI             = np.arctan(H / L)
    OMEGA_SQUARED   = 3 * G * np.cos(PHI) / (2 * L)

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

    init(4.2, 0.5)
    spacings    = np.linspace(1.5, 4)
    velocities  = np.array(list(map(velocity, spacings)))
    RESULT.append(dict(x=spacings, y=velocities))

    if not FIGURE:
        FIGURE = plt.gcf()
    plt.plot(spacings, velocities,
             label="Stronge \& Shu \'88 - Friction = %s" % WITH_FRICTION)
    #  plt.legend()


if __name__ == "__main__":
    main()
