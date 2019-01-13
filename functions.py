from typing import Any, Union

from aircraft_params import *
import math


def aerodynamic_forces_moments(current_states, current_inputs):
    V = current_states[3]

    delta = [current_inputs[0], current_inputs[1]]
    rpm = [current_inputs[2], current_inputs[3]]

    d_f_x_rpm2 = np.array([0.0, 0.0])
    d_m_x_0 = np.array([0.0, 0.0])
    d_m_x_delta = np.array([0.0, 0.0])
    d_m_y_delta = np.array([0.0, 0.0])
    f_x = f_y = f_z = m_x = m_y = m_z = [0.0, 0.0]

    helper_f_x_rpm2 = np.array([1, V/(rpm_nom_cruise / 60)])

    # calculate separate forces and moments
    for i in range(2):
        helper_m_x_0 = np.array([rpm[i] * rpm[i], V*rpm[i]])
        helper_m_x_y_delta = np.array([V*V, rpm[i] * rpm[i], rpm[i]*V])

        d_f_x_rpm2[i] = np.dot(coeff_f_x_rpm2, helper_f_x_rpm2)
        d_m_x_0[i] = np.dot(coeff_m_x_0, helper_m_x_0)
        d_m_x_delta[i] = np.dot(coeff_m_x_delta, helper_m_x_y_delta)
        d_m_y_delta[i] = np.dot(coeff_m_y_delta, helper_m_x_y_delta)

        f_x[i] = d_f_x_rpm2[i] * rpm[i] * rpm[i]
        m_x[i] = d_m_x_0 + d_m_x_delta * delta[i]
        m_y[i] = d_m_y_delta * delta[i]

        f_y[i] = 0
        f_z[i] = 0
        m_z[i] = 0

    f_x = f_x[0] + f_x[1]
    f_y = f_y[0] + f_y[1]
    f_z = f_z[0] + f_z[1]
    m_x = m_x[0] + m_x[1]
    m_y = m_y[0] + m_y[1]
    m_z = m_z[0] + m_z[1]
    forces_moments = [f_x, f_y, f_z, m_x, m_y, m_z]
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
    w: Union[float, Any] = V * math.sin(alpha) * math.cos(beta)

    # intermediate state differentials
    u_dot = r * v - q * w - g * math.sin(theta) + F_M_aero[0] / mass
    v_dot = p * w - r * u + g * math.sin(phi) * math.cos(theta) + F_M_aero[1] / mass
    w_dot = q * u - p * v + g * math.cos(phi) * math.cos(theta) + F_M_aero[2] / mass
    
    # state differentials
    V_dot = (u * u_dot + v * v_dot + w * w_dot) / V  # airspeed
    beta_dot = (V * v_dot - v * V_dot) / (V ** 2 * math.cos(beta))
    alpha_dot = (u * w_dot - w * u_dot) / (u ** 2 + w ** 2)

    I1 = Ixz * (Iyy - Ixx - Izz)
    I2 = (Ixx * Izz - Ixz ** 2)
    p_dot = (Izz * F_M_aero[3] + Ixz * F_M_aero[5] - (I1 * p + (Ixz ** 2 + Izz * (Izz - Iyy)) * r) * q) / I2
    q_dot = (F_M_aero[4] - (Ixx - Izz) * p * r - Ixz * (p ** 2 - r ** 2)) / Iyy  # neglecting thrusting moments
    r_dot = (Ixz * F_M_aero[3] + Ixx * F_M_aero[5] + (I1 * r + (Ixz ** 2 + Ixx * (Ixx - Iyy)) * p) * q) / I2

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

