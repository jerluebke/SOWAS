# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt


L               = 0
H               = 0
SPACING         = 0
LENGTH          = 0
PIECES          = 0
ETA             = 0
PHI             = 0
PSI             = 0
D_THETA         = 0
OMEGA_SQUARED   = 0
THETA_HAT       = 0

INT_STEPS       = 50
PHI_DOT_VALS    = None
INITIAL         = 1
MU              = 0.1
REL_ENERGY_LOSS = 0.9

G = 9.80665


def k(theta, index):
    pieces = index if index < PIECES else PIECES 
    return 1 + np.sum([np.prod(theta_dot_rel(j, theta)**2)
                       for j in range(pieces)])

def theta_dot_rel(index, theta_initial) -> np.ndarray:
    thetas = np.empty(index + 1)
    thetas[0] = theta_initial
    for i in range(1, thetas.size):
        thetas[i] = np.arcsin(ETA * np.cos(thetas[i-1]) - H/L) + thetas[i-1]
    a = np.cos(thetas[1:] - thetas[:-1]) - ETA * np.sin(thetas[:-1]) - MU * H
    b = np.cos(thetas[1:] - thetas[:-1]) + MU * np.sin(thetas[1:] - thetas[:-1])
    return a/b

def P_over_K(theta, phi_dot):
    return 2 * OMEGA_SQUARED * (np.cos(PHI) - np.cos(theta - PHI)) \
            / phi_dot**2 - REL_ENERGY_LOSS

def phi_dot(initial):
    result = np.empty(LENGTH)
    result[0] = initial
    for i in range(1, LENGTH):
        if i <= PIECES:
            k0 = k(0, i)
        result[i] = result[i-1]*np.sqrt((k0-1)/k0*(1+P_over_K(THETA_HAT,
                                                              result[i-1])/k0))
    return result

def theta_dot(thetas, index):
    kt = np.array([k(theta, index) for theta in thetas])
    P_K = P_over_K(thetas, PHI_DOT_VALS[index])
    return PHI_DOT_VALS[index]*np.sqrt(kt/(kt-1)*(1+P_K/kt))

def time(index):
    theta_range = np.arange(0, PSI, D_THETA)
    # prevent occasional floating point error which influences the result
    if theta_range.size == INT_STEPS +1:
        theta_range = theta_range[:-1]
    # Integration of 1/theta_dot
    return np.sum(D_THETA / theta_dot(theta_range, index))

def velocities():
    return (SPACING + H) / np.array([time(i) for i in range(LENGTH)])


def init(height, width, spacing, length, initial, energy_loss, pieces=6):
    global L, H, SPACING, LENGTH, PIECES, ETA, PHI, PSI, D_THETA
    global OMEGA_SQUARED, THETA_HAT, PHI_DOT_VALS, REL_ENERGY_LOSS
    L               = height
    H               = width
    SPACING         = spacing
    LENGTH          = length
    PIECES          = pieces
    ETA             = (SPACING + H) / L
    PHI             = np.arctan(H / L)
    PSI             = np.arcsin(SPACING / L)
    D_THETA         = PSI / INT_STEPS
    OMEGA_SQUARED   = 3 * G * np.cos(PHI) / (2 * L)
    THETA_HAT       = np.arccos(H / (H + SPACING))
    REL_ENERGY_LOSS = energy_loss
    PHI_DOT_VALS    = phi_dot(initial)

def main():
    init(4.2, 0.6, 3, 30, INITIAL)
    pos = np.arange(0, LENGTH*(SPACING+H), SPACING+H)
    vel = velocities()
    plt.gcf()
    plt.plot(pos, vel)
