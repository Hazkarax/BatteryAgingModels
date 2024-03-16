import customtkinter
import tkinter

class RadioButton:
    def __init__(self, parent, i, j, var_list):
        self.parent = parent
        self.i = i
        self.j = j
        self.var_list = var_list
        self.var = var_list[i]
        self.button = customtkinter.CTkRadioButton(parent, text="", value=self.j, variable=self.var, command=self.on_click)
        self.button.grid(row=3 + self.i, column=1 + self.j, sticky="E" if self.j == 0 else "S", padx=8)
    
    def on_click(self):
        print(f"Radio button clicked: i={self.i}, j={self.j}, value={self.var.get()}")

root = customtkinter.CTk()
root.title("Battery Aging Model")
customtkinter.set_appearance_mode("Dark")
customtkinter.set_default_color_theme("dark-blue")

# Create a tabview for the different driving cycles
vehicle_tab = customtkinter.CTkTabview(master=root)
vehicle_tab.grid(row=1, column=0, columnspan=5)
vehicle_tab.add("Cycle 1")
vehicle_tab.add("Cycle 2")

# Create IntVar lists for each cycle
var_list_cycle1 = [tkinter.IntVar(value=2) for _ in range(24)]
var_list_cycle2 = [tkinter.IntVar(value=2) for _ in range(24)]

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
        RadioButton(vehicle_tab.tab("Cycle 1"), i, j, var_list_cycle1)
    
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
        RadioButton(vehicle_tab.tab("Cycle 2"), i, j, var_list_cycle2)
    
    hour_soc = customtkinter.CTkLabel(vehicle_tab.tab("Cycle 2"), text="# [%]")
    hour_soc.grid(row=3 + i, column=4, sticky="E", padx=8)

root.mainloop()
