import matplotlib.pyplot as plt
from functions import aerodynamic_forces_moments
from aircraft_params import *

# set some simulations parameters
d_t = 1  # time step
t_end = 10  # duration

# set initial states
pos_0 = [0.0, 0.0, 0.0]
vel_0 = [8.0, 0.0, 0.0]
orient_0 = [0.0, 0.0, 0.0]
bodyrates_0 = [0.0, 0.0, 0.0]
x_0 = [pos_0[0], pos_0[1], pos_0[2], vel_0[0], vel_0[1], vel_0[2], orient_0[0], orient_0[1], orient_0[2],
       bodyrates_0[0], bodyrates_0[1], bodyrates_0[2]]


u_0 = [0, 0, 10000, 10000]


# start simulation
x = x_0
u = u_0
t = 0

t_vec = [0]  # initialize array to store time stamps
x_array = np.array([x_0])  # initialize array to store states

while t < t_end:
    # calculate forces and moments with current states and control inputs
    curent_forces_moments = aerodynamic_forces_moments(x, u)

    # calculate states derivatives
    d_pos = [x[3] * 1, x[4] * 1, x[5] * 1] * d_t
    d_vel = [curent_forces_moments[0] / mass, curent_forces_moments[1] / mass, curent_forces_moments[2] / mass] * d_t
    d_orient = [0, 0, 0, 0] * d_t
    d_br = [curent_forces_moments[3] / Ixx, curent_forces_moments[4] / Iyy, curent_forces_moments[5] / Izz] * d_t
    d_x = [d_pos[0], d_pos[1], d_pos[2], d_vel[0], d_vel[1], d_vel[2],
           d_orient[0], d_orient[1], d_orient[2], d_br[0], d_br[1], d_br[2]]

    # update sates
    for j in range(len(x)):
        x[j] += d_x[j]

    t += d_t
    t_vec.append(t)
    # print(x_array.shape)
    # print("x: " + str(x_array.shape))
    x_array = np.vstack((x_array, x))


plt.plot(t_vec, x_array[:, 3])
plt.show()


# X = np.linspace(-np.pi, np.pi, 256, endpoint=True)
# C, S = np.cos(X), np.sin(X)
#
# plt.plot(X, C)
# plt.plot(X, S)
#
# plt.show()