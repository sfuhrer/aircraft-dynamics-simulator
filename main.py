import matplotlib.pyplot as plt
from functions import aerodynamic_forces_moments
from functions import calculate_state_differentials
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
u_array = np.array([u_0])  # initialize array to store inputs

while t < t_end:
    # calculate forces and moments with current states and control inputs
    current_aero_forces_moments = aerodynamic_forces_moments(x, u)

    # calculate states derivatives
    d_x = calculate_state_differentials(current_aero_forces_moments, x)

    # update input vector
    u = u_0

    # update states
    for j in range(len(x)):
        x[j] += d_x[j] * d_t

    t += d_t
    t_vec.append(t)
    # print(x_array.shape)
    # print("x: " + str(x_array.shape))
    x_array = np.vstack((x_array, x))
    u_array = np.vstack((u_array, u))

print("states after simulation: " + str(x))

# plotting
# figure with longitudinal states and inputs
# plot velocity


plt.rcParams.update({'font.size': 20})
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
plt.ylabel('alpha [°]')
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

# X = np.linspace(-np.pi, np.pi, 256, endpoint=True)
# C, S = np.cos(X), np.sin(X)
#
# plt.plot(X, C)
# plt.plot(X, S)
#
# plt.show()