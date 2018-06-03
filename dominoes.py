#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import math
import numpy as np
import matplotlib.pyplot as plt

def velocity():
    return (LAMBDA + H) / time()

def time():
    result = 0
    theta = 0
    while theta <= PSI:
        result += D_THETA / theta_dot(theta)
        theta += D_THETA
    return result

def theta_dot(theta):
    k_value = k(theta)
    P_over_K_value = P_over_K(theta)
    return PSI_DOT * math.sqrt(k_value / (k_value - 1)
            * (1 + P_over_K_value / k_value))

def k(theta, theta_initial=0):
    for j in range(1, PIECES):
        theta_i = theta_initial
        theta_dot_rel_prod = 1
        for i in range(j):
            theta_dot_rel_prod = theta_dot_rel(theta_i)**2
