from functions import aerodynamic_forces_moments
from functions import calculate_state_differentials
from functions import plot_states_and_inputs
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

plot_states_and_inputs(t_vec, x_array, u_array)

# X = np.linspace(-np.pi, np.pi, 256, endpoint=True)
# C, S = np.cos(X), np.sin(X)
#
# plt.plot(X, C)
# plt.plot(X, S)
#
# plt.show()