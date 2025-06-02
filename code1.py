import customtkinter as ctk
import csv
import os
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

filename = "employee_data.csv"
data_list = []
current_index = 0

def load_data():
    global data_list
    if os.path.isfile(filename):
        with open(filename, newline='') as f:
            reader = csv.DictReader(f)
            data_list = list(reader)

def show_data(index):
    if 0 <= index < len(data_list):
        row = data_list[index]
        name_var.set(row['Name'])
        address_var.set(row['Address'])
        dob_var.set(row['DOB'])
        gender_var.set(row['Gender'])
        department_var.set(row['Department'])
        email_var.set(row['Email'])
        salary_var.set(row['Salary PA'])

def next_record():
    global current_index
    if current_index < len(data_list) - 1:
        current_index += 1
        show_data(current_index)

def previous_record():
    global current_index
    if current_index > 0:
        current_index -= 1
        show_data(current_index)

def save_data():
    data = [
        name_var.get(),
        address_var.get(),
        dob_var.get(),
        gender_var.get(),
        department_var.get(),
        email_var.get(),
        salary_var.get()
    ]
    file_exists = os.path.isfile(filename)
    with open(filename, 'a', newline='') as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["Name", "Address", "DOB", "Gender", "Department", "Email", "Salary PA"])
        writer.writerow(data)
    load_data()
    for var in [name_var, address_var, dob_var, gender_var, department_var, email_var, salary_var]:
        var.set("")

def plot_salary_graph():
    if not data_list:
        return
    names = [row['Name'] for row in data_list]
    try:
        salaries = [float(row['Salary PA']) for row in data_list]
    except ValueError:
        salaries = [0 for _ in data_list]  # fallback if parsing fails

    graph_window = ctk.CTkToplevel(root)
    graph_window.title("Employee Salary Line Graph")
    graph_window.geometry("600x400")

    fig, ax = plt.subplots(figsize=(6, 4))
    ax.plot(names, salaries, marker='o')
    ax.set_title("Employee Salaries")
    ax.set_xlabel("Employee Name")
    ax.set_ylabel("Salary (PA)")
    ax.tick_params(axis='x', rotation=45)

    canvas = FigureCanvasTkAgg(fig, master=graph_window)
    canvas.draw()
    canvas.get_tk_widget().pack(fill='both', expand=True)

# Set theme and appearance
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# GUI Setup
root = ctk.CTk()
root.title("Employee Data Entry")
root.geometry("500x650")

name_var = ctk.StringVar()
address_var = ctk.StringVar()
dob_var = ctk.StringVar()
gender_var = ctk.StringVar()
department_var = ctk.StringVar()
email_var = ctk.StringVar()
salary_var = ctk.StringVar()

fields = [
    ("Name", name_var),
    ("Address", address_var),
    ("DOB", dob_var),
    ("Email", email_var),
    ("Salary PA", salary_var)
]

for label, var in fields:
    ctk.CTkLabel(root, text=label).pack(pady=4)
    ctk.CTkEntry(root, textvariable=var, width=300).pack()

ctk.CTkLabel(root, text="Gender").pack(pady=4)
gender_cb = ctk.CTkComboBox(root, variable=gender_var, values=["Male", "Female"])
gender_cb.pack()

ctk.CTkLabel(root, text="Department").pack(pady=4)
department_cb = ctk.CTkComboBox(root, variable=department_var,
                                values=["HR", "Finance", "IT", "Marketing", "Sales"])
department_cb.pack()

ctk.CTkButton(root, text="Save", command=save_data).pack(pady=10)
ctk.CTkButton(root, text="Previous", command=previous_record).pack(pady=5)
ctk.CTkButton(root, text="Next", command=next_record).pack(pady=5)
ctk.CTkButton(root, text="Show Salary Graph", command=plot_salary_graph).pack(pady=10)

load_data()
if data_list:
    show_data(current_index)

root.mainloop()
