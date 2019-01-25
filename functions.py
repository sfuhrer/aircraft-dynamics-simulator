from typing import Any, Union
import matplotlib.pyplot as plt
from aircraft_params import *
import math


def aerodynamic_forces_moments(current_states, current_inputs):
    V = current_states[3]

    delta = [current_inputs[0], current_inputs[1]]
    rpm = [current_inputs[2], current_inputs[3]]

    helper_f_x_rpm2 = np.array([1, V / (rpm_nom_cruise / 60.0)])
    helper_m_x_0_0 = np.array([rpm[0] ** 2, V * rpm[0]])
    helper_m_x_0_1 = np.array([rpm[1] ** 2, V * rpm[1]])
    helper_m_x_y_delta_0 = np.array([V ** 2, rpm[0] ** 2, rpm[0] * V])
    helper_m_x_y_delta_1 = np.array([V ** 2, rpm[1] ** 2, rpm[1] * V])

    d_f_x_rpm2 = np.dot(coeff_f_x_rpm2, helper_f_x_rpm2)
    d_m_x_0_0 = np.dot(coeff_m_x_0, helper_m_x_0_0)
    d_m_x_0_1 = np.dot(coeff_m_x_0, helper_m_x_0_1) * (-1)
    d_m_x_delta_0 = np.dot(coeff_m_x_delta, helper_m_x_y_delta_0)
    d_m_x_delta_1 = np.dot(coeff_m_x_delta, helper_m_x_y_delta_1) * (-1)
    d_m_y_delta_0 = np.dot(coeff_m_y_delta, helper_m_x_y_delta_0)
    d_m_y_delta_1 = np.dot(coeff_m_y_delta, helper_m_x_y_delta_1)

    f_x = [d_f_x_rpm2 * rpm[0] ** 2, d_f_x_rpm2 * rpm[1] ** 2]
    m_x = [d_m_x_0_0 + d_m_x_delta_0*delta[0], d_m_x_0_1 + d_m_x_delta_1*delta[1]]
    m_y = [d_m_y_delta_0 * delta[0], d_m_y_delta_1 * delta[1]]

    f_x_combined = f_x[0] + f_x[1]
    f_y_combined = 0.0
    f_z_combined = 0.0
    m_x_combined = m_x[0] + m_x[1]
    m_y_combined = m_y[0] + m_y[1]
    m_z_combined = (f_x[0] - f_x[1]) * l_y
    forces_moments = [f_x_combined, f_y_combined, f_z_combined, m_x_combined, m_y_combined, m_z_combined]
    return forces_moments


def calculate_state_differentials(F_M_aero, states):

    # states
    V = states[3]  # airspeed
    beta = states[4]  # sideslip angle
    alpha = states[5]  # angle of attack
    p = states[6]  # roll rate
    q = states[7]  # pitch rate
    r = states[8]  # yaw rate
    phi = states[9]  # roll angle
    theta = states[10]  # pitch angle
    psi = states[11]  # flight path angle

    #  intermediate states
    u = V * math.cos(alpha) * math.cos(beta)
    v = V * math.sin(beta)
    w = V * math.sin(alpha) * math.cos(beta)

    # intermediate state differentials
    u_dot = r * v - q * w - g * math.sin(theta) + F_M_aero[0] / mass
    v_dot = p * w - r * u + g * math.sin(phi) * math.cos(theta) + F_M_aero[1] / mass
    w_dot = q * u - p * v + g * math.cos(phi) * math.cos(theta) + F_M_aero[2] / mass
    
    # state differentials
    V_dot = (u * u_dot + v * v_dot + w * w_dot) / V  # airspeed
    beta_dot = (V * v_dot - v * V_dot) / (V**2 * math.cos(beta))
    alpha_dot = (u * w_dot - w * u_dot) / (u**2 + w**2)

    I1 = Ixz * (Iyy - Ixx - Izz)
    I2 = (Ixx * Izz - Ixz ** 2)
    p_dot = (Izz * F_M_aero[3] + Ixz * F_M_aero[5] - (I1 * p + (Ixz**2 + Izz * (Izz - Iyy)) * r) * q) / I2
    q_dot = (F_M_aero[4] - (Ixx - Izz) * p * r - Ixz * (p**2 - r**2)) / Iyy  # neglecting thrusting moments
    r_dot = (Ixz * F_M_aero[3] + Ixx * F_M_aero[5] + (I1 * r + (Ixz**2 + Ixx * (Ixx - Iyy)) * p) * q) / I2

    phi_dot = p + (q * math.sin(phi) + r * math.cos(phi)) * math.tan(theta)
    theta_dot = q * math.cos(phi) - r * math.sin(phi)
    psi_dot = (q * math.sin(phi) + r * math.cos(phi)) / math.cos(theta)

    n_dot = u * math.cos(theta) * math.cos(psi) + v * \
            (math.sin(phi) * math.sin(theta) * math.cos(psi) - math.cos(phi) * math.sin(psi)) + \
            w * (math.sin(phi) * math.sin(psi) + math.cos(phi) * math.sin(theta) * math.cos(psi))
    e_dot = u * math.cos(theta) * math.sin(psi) + v * \
            (math.cos(phi) * math.cos(psi) + math.sin(phi) * math.sin(theta) * math.sin(psi)) + w * \
            (math.cos(phi) * math.sin(theta) * math.sin(psi) - math.sin(phi) * math.cos(psi))

    d_dot = -u * math.sin(theta) + v * math.sin(phi) * math.cos(theta) + w * math.cos(phi) * math.cos(theta)

    state_differentials = [n_dot, e_dot, d_dot, V_dot, alpha_dot, beta_dot,
                           p_dot, q_dot, r_dot, phi_dot, theta_dot, psi_dot]

    return state_differentials


def plot_states_and_inputs(t_vec, x_array, u_array):
    # plotting
    # figure with longitudinal states and inputs

    # plot velocity
    plt.rcParams.update({'font.size': 10})
    plt.figure(figsize=(30, 30))
    plt.subplot(4, 3, 1)
    plt.plot(t_vec, x_array[:, 3])
    plt.ylabel('V [m/s]')
    plt.xlabel('time [s]')

    # plot of AoA
    plt.subplot(4, 3, 4)
    plt.plot(t_vec, x_array[:, 4])
    plt.ylabel('alpha [°]')
    plt.xlabel('time [s]')

    # plot of pitch
    plt.subplot(4, 3, 7)
    plt.plot(t_vec, x_array[:, 10])
    plt.ylabel('pitch [°]')
    plt.xlabel('time [s]')

    # inputs
    # plot elevon left input
    plt.subplot(4, 3, 2)
    plt.plot(t_vec, u_array[:, 0])
    plt.ylabel('elevon left[°]')
    plt.xlabel('time [s]')

    # plot elevon right input
    plt.subplot(4, 3, 5)
    plt.plot(t_vec, u_array[:, 1])
    plt.ylabel('elevon right[°]')
    plt.xlabel('time [s]')

    # plot throttle left input
    plt.subplot(4, 3, 8)
    plt.plot(t_vec, u_array[:, 2])
    plt.ylabel('throttle left[rpm]')
    plt.xlabel('time [s]')

    # plot throttle left input
    plt.subplot(4, 3, 11)
    plt.plot(t_vec, u_array[:, 3])
    plt.ylabel('throttle right[rpm]')
    plt.xlabel('time [s]')

    # plot of lateral states
    # plot of beta
    plt.subplot(4, 3, 3)
    plt.plot(t_vec, x_array[:, 5])
    plt.ylabel('beta [°]')
    plt.xlabel('time [s]')

    # plot of roll
    plt.subplot(4, 3, 6)
    plt.plot(t_vec, x_array[:, 9])
    plt.ylabel('roll [°]')
    plt.xlabel('time [s]')

    plt.show()
