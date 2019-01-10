l_x = 0.12
l_y = 0.14

c_F_T_rpm2 = 8.0e-09
c_F_T_v_rpm = -6.4e-08

c_M_x_rpm2 = 4.7e-10
c_M_x_v_rpm = -2.2e-07

c_M_x_v2_delta = 1.1e-04
c_M_x_rpm2_delta = 6.1e-11
c_M_x_v_rpm_delta = -2.9e-08

c_M_y_v2_delta = -9.6e-05
c_M_y_rpm2_delta = -5.2e-11
c_M_y_v_rpm_delta = 2.5e-08



coeff_F_x_rpm2 = [c_F_T_rpm2, c_F_T_v_rpm]
coeff_M_y_delta	= [c_M_y_v2_delta, c_M_y_rpm2_delta, c_M_y_v_rpm_delta]
coeff_M_x_0 = [c_M_x_rpm2, c_M_x_v_rpm]
coeff_M_x_delta = [c_M_x_v2_delta, c_M_x_rpm2_delta, c_M_x_v_rpm_delta]



# geometry
S_wing = 0.47  # wing surface[m ^ 2]
b_wing = 2.59  # wingspan[m]
c_chord = 0.180  # mean chord length[m]

# mass / inertia
mass = 2.65  # total mass of airplane[kg]
Ixx = 0.1512 * 1.1  # inertias [kg m ^ 2]
Iyy = 0.2785 * 1.4  # inertias[kg m ^ 2]
Izz = 0.3745 * 1.4  # inertias[kg m ^ 2]
Ixz = 0.0755  # inertias[kg m ^ 2]

# environment
g = 9.81  # gravitational acceleration[m / s ^ 2]
rho_air = 1.18  # air density


