from functions import aerodynamic_forces_moments
from functions import calculate_state_differentials
from functions import plot_states_and_inputs
from aircraft_params import *
# from tkinter import *
import tkinter
import tkinter.messagebox


states_list = 'V [m/s]', 'alpha [°]', 'beta [°]', 'pitch [°]', 'roll [°]'
states_defaults = [10, 0, 0, 0, 0]
inputs_list = 'delta_0 [°]', 'delta_1 [°]', 'rpm_0 [rpm]', 'rpm_1 [rpm]'
inputs_defaults = [0, 0, 8000, 8000]


def make_entryfields(frame, fields, defaults):
    entries = []
    for idx, field in enumerate(fields):
        row = tkinter.Frame(frame)  # makes a new frame for every state
        lab = tkinter.Label(row, width=15, text=field)
        ent = tkinter.Entry(row)
        row.pack(side=tkinter.TOP, fill=tkinter.X, padx=5, pady=5)  # new frame = state: put below the one before
        lab.pack(side=tkinter.LEFT)
        ent.pack(side=tkinter.LEFT, fill=tkinter.X)
        ent.insert(10, defaults[idx])
        #ent.pack(side=tkinter.RIGHT, expand=tkinter.YES, fill=tkinter.X)
        entries.append((field, ent))
    return entries


def make_textfields(frame, fields, defaults):
    entries = []
    for idx, field in enumerate(fields):
        row = tkinter.Frame(frame)  # makes a new frame for every state
        lab = tkinter.Label(row, width=15, text=field)
        txt = tkinter.Text(row, height=1, width=10)
        row.pack(side=tkinter.TOP, fill=tkinter.X, padx=5, pady=5)  # new frame = state: put below the one before
        lab.pack(side=tkinter.LEFT)
        txt.pack(side=tkinter.LEFT, fill=tkinter.X)
        txt.insert(tkinter.END, defaults[idx])
        entries.append((field, txt))
    return entries


def make_inputs(root_frame, fields, defaults):
    inpts = []
    for idx, field in enumerate(fields):
        row = tkinter.Frame(root_frame)  # makes a new frame for every state
        lab = tkinter.Label(row, width=15, text=field, anchor='w')
        if idx < 2:  # for the deltas
            scale = tkinter.Scale(row, from_=-45, to=45, tickinterval=15, length=200, orient=tkinter.HORIZONTAL)
        else:  # for the rpms
            scale = tkinter.Scale(row, from_=0, to=14000, tickinterval=7000, length=200, orient=tkinter.HORIZONTAL)

        scale.set(defaults[idx])
        row.pack(side=tkinter.TOP, fill=tkinter.X, padx=5, pady=5)  # new frame = state: put below the one before
        lab.pack(side=tkinter.LEFT)
        scale.pack(side=tkinter.LEFT, fill=tkinter.X)
        inpts.append((field, scale))
    return inpts


def fetch_numbers(entries):
    ret = []
    for entry in entries:
        field = entry[0]
        text = float(entry[1].get())
        ret.append(text)
        # print('%s: "%s"' % (field, text))
    return ret


def callback_calc():
    results = []
    x = fetch_numbers(entries)  # read states
    u = fetch_numbers(input_scales)  # read inputs (from scales)
    forces_moments = aerodynamic_forces_moments(x, u)
    for idx, result_field in enumerate(res_disp):
        result_field[1].delete(1.0, 'end')
        result_field[1].insert('end', round(forces_moments[idx], 4))


# set up GUI
root = tkinter.Tk()
root.title("Static Forces and Moments Calculator")
root.geometry("1000x500")

# make labels and textfields for states input
states_frame = tkinter.Frame(root)
# states_frame.pack(side=tkinter.LEFT)
states_frame.grid(row=0, column=0)
entries = make_entryfields(states_frame, states_list, states_defaults)

# make slides for control inputs input
input_frame = tkinter.Frame(root)
input_frame.grid(row=0, column=1)
# input_frame.pack(side=tkinter.LEFT)
input_scales = make_inputs(input_frame, inputs_list, inputs_defaults)

# display results
results_frame = tkinter.Frame(root)
results_frame.grid(row=0, column=2)
# results_frame.pack(side=tkinter.LEFT)
res_name = 'F_x [N]', 'F_y [N]', 'F_z [N]', 'M_x [Nm]', 'M_y [Nm]', 'M_z [Nm]'
res_default = [0, 0, 0, 0, 0, 0]
res_disp = make_textfields(results_frame, res_name, res_default)
calc_button = tkinter.Button(results_frame, text='Calc', command=callback_calc).pack()


root.mainloop()
