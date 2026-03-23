import tkinter as tk
from tkinter import messagebox
import random
import math
import matplotlib.pyplot as plt

employees = []

# --------------------------
# Employee Class
# --------------------------
class Employee:
    def __init__(self, name, workload):
        self.name = name
        self.workload = workload

    def __repr__(self):
        return f"{self.name}({self.workload})"


# --------------------------
# Clash Function
# --------------------------
def clash(schedule):
    return sum(schedule[i].workload * schedule[i+1].workload
               for i in range(len(schedule)-1))


# --------------------------
# Generate Neighbor
# --------------------------
def neighbor(schedule):
    new_schedule = schedule[:]
    i = random.randint(0, len(schedule)-2)
    new_schedule[i], new_schedule[i+1] = new_schedule[i+1], new_schedule[i]
    return new_schedule


# --------------------------
# Hill Climbing
# --------------------------
def hill_climbing(schedule):
    current = schedule[:]

    while True:
        new = neighbor(current)

        if clash(new) < clash(current):
            current = new
        else:
            break

    return current


# --------------------------
# Random Restart
# --------------------------
def random_restart(schedule, restarts=10):

    best = schedule[:]

    for _ in range(restarts):

        temp = schedule[:]
        random.shuffle(temp)

        result = hill_climbing(temp)

        if clash(result) < clash(best):
            best = result

    return best


# --------------------------
# Simulated Annealing
# --------------------------
def simulated_annealing(schedule):

    current = schedule[:]
    temperature = 1000
    cooling = 0.95

    while temperature > 1:

        new = neighbor(current)

        diff = clash(new) - clash(current)

        if diff < 0 or random.random() < math.exp(-diff/temperature):
            current = new

        temperature *= cooling

    return current


# --------------------------
# Add Employee
# --------------------------
def add_employee():

    name = name_entry.get()
    workload = workload_entry.get()

    if name == "" or workload == "":
        messagebox.showerror("Error", "Enter valid data")
        return

    try:
        workload = int(workload)
    except:
        messagebox.showerror("Error", "Workload must be a number")
        return

    emp = Employee(name, workload)
    employees.append(emp)

    listbox.insert(tk.END, f"{name} ({workload})")

    name_entry.delete(0, tk.END)
    workload_entry.delete(0, tk.END)


# --------------------------
# Run Optimization
# --------------------------
def optimize():

    if len(employees) < 2:
        messagebox.showerror("Error", "Enter at least 2 employees")
        return

    hc = hill_climbing(employees)
    rr = random_restart(employees)
    sa = simulated_annealing(employees)

    hc_score = clash(hc)
    rr_score = clash(rr)
    sa_score = clash(sa)

    result_text.delete(1.0, tk.END)

    result_text.insert(tk.END, "Hill Climbing:\n")
    result_text.insert(tk.END, f"{hc}\nScore: {hc_score}\n\n")

    result_text.insert(tk.END, "Random Restart:\n")
    result_text.insert(tk.END, f"{rr}\nScore: {rr_score}\n\n")

    result_text.insert(tk.END, "Simulated Annealing:\n")
    result_text.insert(tk.END, f"{sa}\nScore: {sa_score}\n\n")

    show_graph(hc_score, rr_score, sa_score)

    save_result(hc, hc_score)


# --------------------------
# Graph Visualization
# --------------------------
def show_graph(hc, rr, sa):

    algorithms = ["Hill Climbing", "Random Restart", "Simulated Annealing"]
    scores = [hc, rr, sa]

    plt.bar(algorithms, scores)

    plt.title("Algorithm Performance Comparison")
    plt.ylabel("Clash Score")

    plt.show()


# --------------------------
# Save Output
# --------------------------
def save_result(schedule, score):

    with open("optimized_schedule.txt", "w") as f:

        f.write("Optimized Schedule\n\n")

        for emp in schedule:
            f.write(f"{emp.name} - {emp.workload}\n")

        f.write(f"\nClash Score: {score}")


# --------------------------
# GUI
# --------------------------

root = tk.Tk()
root.title("Employee Shift Optimization")

tk.Label(root, text="Employee Name").grid(row=0, column=0)
tk.Label(root, text="Workload").grid(row=1, column=0)

name_entry = tk.Entry(root)
workload_entry = tk.Entry(root)

name_entry.grid(row=0, column=1)
workload_entry.grid(row=1, column=1)

tk.Button(root, text="Add Employee", command=add_employee).grid(row=2, column=0, columnspan=2)

listbox = tk.Listbox(root, width=30)
listbox.grid(row=3, column=0, columnspan=2)

tk.Button(root, text="Optimize Schedule", command=optimize).grid(row=4, column=0, columnspan=2)

result_text = tk.Text(root, height=10, width=40)
result_text.grid(row=5, column=0, columnspan=2)

root.mainloop()
