import customtkinter
import tkinter
from CTkMessagebox import CTkMessagebox
import calculation

#TODO: Error message if End-Of-Day SOC ≠ Initial SOC

root = customtkinter.CTk()
root.title("Battery Aging Model")
customtkinter.set_appearance_mode("Dark")
customtkinter.set_default_color_theme("dark-blue")

## GUI ##

# Initial setting frame
settings_frame = customtkinter.CTkFrame(master=root)
settings_frame.grid(row=0, column=0)

# Add the SOC
init_soc_label = customtkinter.CTkLabel(master=settings_frame, text="Base SOC:")
init_soc_label.grid(row=0, column=0, padx=15, pady=7)

init_soc_entry = customtkinter.CTkEntry(master=settings_frame, placeholder_text="80%")
init_soc_entry.grid(row=0, column=1)

# Automatically retrieved
# init_soc_btn = customtkinter.CTkButton(master=settings_frame, text="Set")
# init_soc_btn.grid(row=0, column=2, padx=15)

# Add C-rate of the battery
c_rate_label = customtkinter.CTkLabel(master=settings_frame, text="C-rate")
c_rate_label.grid(row=1, column=0, padx=15, pady=7)

c_rate_entry = customtkinter.CTkEntry(master=settings_frame, placeholder_text="0.2")
c_rate_entry.grid(row=1, column=1)

sim_days_label = customtkinter.CTkLabel(master=settings_frame, text="Simulation Days")
sim_days_label.grid(row=1, column=2, padx=10)
sim_days_entry = customtkinter.CTkEntry(master=settings_frame, placeholder_text="30")
sim_days_entry.grid(row=1, column=3, padx=10)

# Automatically retrieved
# c_rate_btn = customtkinter.CTkButton(master=settings_frame, text="Set")
# c_rate_btn.grid(row=1, column=2, padx=15)

class RadioButton:
    def __init__(self, parent, i, j, var_list, global_status_list):
        self.parent = parent
        self.i = i
        self.j = j
        self.var_list = var_list
        self.global_status_list = global_status_list
        self.var = var_list[i]
        self.button = customtkinter.CTkRadioButton(parent, text="", value=self.j, variable=self.var, command=self.on_click)
        self.button.grid(row=3 + self.i, column=1 + self.j, sticky="E" if self.j == 0 else "S", padx=8)
    
    def on_click(self):
        self.global_status_list[self.i] = self.j  # Update the global status list
        #print(f"Radio button clicked: i={self.i}, j={self.j}, value={self.var.get()}")

def calc_soc(global_status_list, n):
    if init_soc_entry.get() == "":
        soc = 80
    else:
        soc = float(init_soc_entry.get())
    if c_rate_entry.get() == "":
        c_rate = 0.2
    else:
        c_rate = float(c_rate_entry.get())

    socs = [] # A list where all the SOC during the cycle are saved

    for h in global_status_list:
        if h == 2: # The battery is idle
            socs.append(soc)
        elif h == 1: # The battery is discharging 
            socs.append(soc - 100 * c_rate)
        elif h == 0: # The battery is charging
            socs.append(soc + 100 * c_rate)
        soc = socs[-1]

    for s in range(24):
        if socs[s] < 0 or socs[s] > 100:
            CTkMessagebox(title="Invalid SOC", message="SOC outside of 0-100% boundary!", icon="cancel")
            break
        else:
            hour_soc = customtkinter.CTkLabel(vehicle_tab.tab(f"Cycle {n}"), text=f"{socs[s]} [%]")
            hour_soc.grid(row=3 + s, column=4)


    if socs[-1] != float(init_soc_entry.get()):
        CTkMessagebox(title="Invalid Daily Cycle", message="Cycle must return to base SOC")
    # elif global_status_list[-1] == 1 and socs[-1] != soc+100*c_rate:
    #     CTkMessagebox(title="Invalid Daily Cycle", message="If Battery ends in discharge, it must equal the initial SOC + C-rate*100")
    # elif global_status_list[-1] == 0 and socs[-1] != soc-100*c_rate:
    #     CTkMessagebox(title="Invalid Daily Cycle", message="If Battery ends in charge, it must equal the initial SOC - C-rate*100")

    
    return(socs)

# Create a tabview for the different driving cycles
vehicle_tab = customtkinter.CTkTabview(master=root)
vehicle_tab.grid(row=1, column=0, columnspan=5)
vehicle_tab.add("Cycle 1")
vehicle_tab.add("Cycle 2")

# Create IntVar lists for each cycle
var_list_cycle1 = [tkinter.IntVar(value=2) for _ in range(24)]
var_list_cycle2 = [tkinter.IntVar(value=2) for _ in range(24)]

# Global lists to store the status of all radio buttons for each cycle
global_status_list1 = [2] * 24  # Initialized with idle status (2) for all hours
global_status_list2 = [2] * 24  # Initialized with idle status (2) for all hours

# Add headers for Cycle 1
headers = ["Hour", "Charging", "Discharging", "Idleing", "SOC"]
for idx, header in enumerate(headers):
    header_label = customtkinter.CTkLabel(vehicle_tab.tab("Cycle 1"), text=header)
    header_label.grid(row=2, column=idx, padx=4)

# Add each hour interval for Cycle 1
for i in range(24):
    hour = f"{i:02d}-{(i+1)%24:02d}"  # Format hour range
    hour_label = customtkinter.CTkLabel(vehicle_tab.tab("Cycle 1"), text=hour + ": ")
    hour_label.grid(row=3 + i, column=0, padx=8)
    
    for j, action in enumerate(["Charging", "Discharging", "Idleing"]):
        RadioButton(vehicle_tab.tab("Cycle 1"), i, j, var_list_cycle1, global_status_list1)
    
    hour_soc = customtkinter.CTkLabel(vehicle_tab.tab("Cycle 1"), text="# [%]")
    hour_soc.grid(row=3 + i, column=4, sticky="E", padx=8)

# Add headers for Cycle 2
for idx, header in enumerate(headers):
    header_label = customtkinter.CTkLabel(vehicle_tab.tab("Cycle 2"), text=header)
    header_label.grid(row=2, column=idx, padx=4)

# Add each hour interval for Cycle 2
for i in range(24):
    hour = f"{i:02d}-{(i+1)%24:02d}"  # Format hour range
    hour_label = customtkinter.CTkLabel(vehicle_tab.tab("Cycle 2"), text=hour + ": ")
    hour_label.grid(row=3 + i, column=0, padx=8)
    
    for j, action in enumerate(["Charging", "Discharging", "Idleing"]):
        RadioButton(vehicle_tab.tab("Cycle 2"), i, j, var_list_cycle2, global_status_list2)
    
    hour_soc = customtkinter.CTkLabel(vehicle_tab.tab("Cycle 2"), text="# [%]")
    hour_soc.grid(row=3 + i, column=4, sticky="E", padx=8)

calculate_frame = customtkinter.CTkFrame(master=root)
calculate_frame.grid(row=2, column=0)

calculate_soc_btn1 = customtkinter.CTkButton(master=calculate_frame, text="Calculate SOC Cycle 1", command=lambda: calc_soc(global_status_list1, 1))
calculate_soc_btn1.grid(row=0, column=0, padx=10, pady=20)

calculate_soc_btn2 = customtkinter.CTkButton(master=calculate_frame, text="Calculate SOC Cycle 2", command=lambda: calc_soc(global_status_list2, 2))
calculate_soc_btn2.grid(row=0, column=1, padx=10, pady=20)

plot_result_btn = customtkinter.CTkButton(master=calculate_frame, text="Plot Results", command=lambda: calculation.calc_deg(calc_soc(global_status_list1, 1), calc_soc(global_status_list2, 2), int(sim_days_entry.get()), global_status_list1, global_status_list2, float(c_rate_entry.get())))
plot_result_btn.grid(row=0, column=2, padx=10, pady=20)

clear_result_btn = customtkinter.CTkButton(master=calculate_frame, text="Clear Results")
clear_result_btn.grid(row=0, column=3, padx=10, pady=20)

root.mainloop()
