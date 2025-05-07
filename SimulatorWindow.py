import tkinter as tk
from tkinter import scrolledtext
from StatzySimulator import StatzySimulator  # Assuming StatzySimulator is defined in StatzySimulator.py

def load_and_run():
    sim.load_program(code_box.get("1.0", tk.END))
    update_status()

def step():
    output = sim.step()
    update_status()
    if output:
        status_label.config(text=output)

def update_status():
    reg_lines = [f"{reg}: {val}" for reg, val in sim.registers.items()]
    pc_line = f"PC: {sim.pc}"
    registers_label.config(text="\n".join(reg_lines + [pc_line]))

def write_output(text):
    output_box.config(state='normal')
    output_box.insert(tk.END, text + "\n")
    output_box.see(tk.END)
    output_box.config(state='disabled')

sim = StatzySimulator(print_callback=write_output)  # Assuming StatzySimulator is defined elsewhere

# GUI Setup
root = tk.Tk()
root.title("Statzy Simulator")

# Create the main horizontal frame
main_frame = tk.Frame(root)
main_frame.pack(fill='both', expand=True)

# Left side: Code box and output box
left_frame = tk.Frame(main_frame)
left_frame.pack(side='left', fill='both', expand=True)

# Add the code box to the left frame
code_box = scrolledtext.ScrolledText(left_frame, height=30, width=70)
code_box.pack(fill='both', expand=True)

# Add the output box to the left frame
output_box = scrolledtext.ScrolledText(left_frame, height=10, width=70, state='disabled')
output_box.pack(fill='both', expand=True)

# Right side: Registers
right_frame = tk.Frame(main_frame, padx=10)
right_frame.pack(side='right', fill='y')

# Display registers to the right frame
registers_label = tk.Label(
    right_frame, 
    text="Registers", 
    font=("Courier", 12), 
    justify='left', 
    anchor='nw'
)
registers_label.pack(fill='both', expand=True)


# Add buttons below the output box
load_button = tk.Button(left_frame, text="Load", command=load_and_run)
load_button.pack(fill='x', pady=5)

step_button = tk.Button(left_frame, text="Step", command=step)
step_button.pack(fill='x', pady=5)

status_label = tk.Label(left_frame, text="Status")
status_label.pack(fill='x', pady=5)

root.mainloop()