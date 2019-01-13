import numpy as np
from aircraft_params import *


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
