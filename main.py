# import tkinter  # all fine
import numpy as np
#import matplotlib.pyplot as plt
#import aircraft_params
from typing import List, Any, Union

from aircraft_params import *

t = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
j = 0
y = [None] * 11
d_t = 1  # timestep
rpm = [2]
pos_0 = [0, 0, 0]
vel_0 = [8, 0, 0]
orient_0 = [0, 0, 0]
bodyrates_0 = [0, 0, 0]

x_0 = [pos_0[0], pos_0[1], pos_0[2], vel_0[0], vel_0[1], vel_0[2], orient_0[0], orient_0[1], orient_0[2],
       bodyrates_0[0], bodyrates_0[1], bodyrates_0[2]]

u_0 = [0, 0, 0, 0]



def aerodynamic_forces_moments(current_states, current_inputs):
    V = current_states[0]


    delta = [current_inputs[0], current_inputs[1]]
    rpm = [current_inputs[2], current_inputs[3]]

    rpm_nom_cruise = 11000

    d_F_x_rpm = [0, 0]
    F_x = F_y = F_z = M_x = M_y = M_z = [0,0]

    """
    print('rpm', rpm[0])
    print('c_F_T_rpm2', c_F_T_rpm2)

    d_F_x_rpm[0] = c_F_T_rpm2 * rpm[0]
    print('d_F_x_rpm', d_F_x_rpm[0])

    F_x[0] = d_F_x_rpm[0] * rpm[0] * rpm[0]
    print('value of F_x:', F_x[0])
    """

    # print('******************')

    helper_F_x = [1, V]

    # calculate separate forces and moments
    for i in range(2):
        d_F_x_rpm[i] = c_F_T_rpm2 * rpm[i]
        # print('d_F_x_rpm', d_F_x_rpm[i])
        F_x[i] = d_F_x_rpm[i] * rpm[i] * rpm[i]
        F_y[i] = 0
        F_z[i] = 0
        M_x[i] = 0
        M_y[i] = 0
        M_z[i] = 0
        # F_x[i] = [coeff_F_x_rpm2 * helper_F_x in
        # a = np.array([1,2,3])

    F_x = F_x[0] + F_x[1]
    F_y = F_y[0] + F_y[1]
    F_z = F_z[0] + F_z[1]
    M_x = M_x[0] + M_x[1]
    M_y = M_y[0] + M_y[1]
    M_z = M_z[0] + M_z[1]
    forces_moments = [F_x, F_y, F_z, M_x, M_y, M_z]
    return forces_moments


x = x_0
u = u_0
t = 0
t_end = 10
t_vec = [0]
x_array = [x_0]

while t < t_end:
    # calculate forces and moments with current states and control inputs
    curent_forces_moments = aerodynamic_forces_moments(x, u)

    # calculate states derrivatives
    d_pos = [x[3] * 1, x[4] * 1, x[5] * 1] * d_t
    d_vel = [curent_forces_moments[0] / mass, curent_forces_moments[1] / mass, curent_forces_moments[2] / mass] * d_t
    d_orient = [0, 0, 0, 0] * d_t
    d_br = [curent_forces_moments[3] / Ixx, curent_forces_moments[4] / Iyy, curent_forces_moments[5] / Izz] * d_t
    d_x = [d_pos[0], d_pos[1], d_pos[2], d_vel[0], d_vel[1], d_vel[2],
           d_orient[0], d_orient[1], d_orient[2], d_br[0], d_br[1], d_br[2]]

    # update sates
    for i in range(len(x)):
        x[i] += d_x[i]

    t +=d_t
    t_vec.append(t)
    x_array.append(x)
    print(t)
    print(x)

# plot(t_vec, x_vec)