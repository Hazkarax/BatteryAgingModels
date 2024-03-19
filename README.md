# Introduction
It is well known that Litium-Ion batteries degrades over time. This behaviour is however been proven to be hard to model, both due to each batteries individual properties, and also since the degradation depends on many types of factors, such as discharge rates, ambient Temperature, Depth of Discharge (DOD), State of Charge (SOC) when idle, time and Voltage.

This program uses two empirical models to modulate the degradation of two specific cycles. The Python GUI can be used to create a daily battery cycle, which is repeated a specific number of days. The program then outputs the degradation graph with the capacity loss of the battery.

This project is created as a part of the Bachelor Thesis "Bi-Directional Charging", pursued by a group of 5 students from Chalmers University of Technology, and 5 from Penn-State University. 

# How to use
The project consists of a Matlab-script and a python GUI. The python GUI has some dependencies.

CustomTkinter (https://github.com/TomSchimansky/CustomTkinter) is used to create a nice looking GUI. It also uses the additional CTkMessagebox (https://github.com/Akascape/CTkMessagebox) to display error messages. These can be installed using:
```console
pip install customtkinter
```
```console
pip install ctkmessagebox
```
Make sure that tkinter is also installed as customtkinter in itself have some dependencies.
```console
pip install tkinter
```

## Running the GUI
Run the program from an IDE or the terminal, from the base directory as follows
```shell script
python3 python_gui/gui.py
```

A lot of functions are not yet implemented in the GUI, such as the "Clear Results" button. The GUI is in its first version, an simply provides to simple plots of the capacity loss.

# Theoretical background
A short introduction to the models, and how it is used. A more thorough background will be published in the finished paper.

## The Empirical Models
In order to accomplish the following, this model combines the results of two scientific studies whom investigates and determines an Empirical model for cyclic aging and calendar aging respectively. The two models are then combined, using Eulers Method, to determine the cell degradation of an NMC cell in a Volkswagen ID.4.

The Calendar equation model, comes from the Conference Paper "Empirical Modeling of Degradation in Litium-ion Batteries and Validation in Complex Scenarios", by Apoorva Roy et. al. The Equation used for calendar aging, are the following for the $5^{\circ} C$  ambient temperature case:

$C_{loss, cal} = (0.09 \cdot SOC+0.01)\cdot \sqrt{t}$

In the $45^{\circ} C$  ambient degree case, the capacity loss is linear:

$C_{loss, cal} = 1+(0.004 \cdot SOC) \cdot t$

The cyclic aging model comes from the Peer-reviewed Journal of Energy Storage, and the article "Empirical Li-ion model derived from single particle model", by Abrina Kathrin Rechkemmer et. al. And states

$C_{loss, cyc} = a_1(t+a_2\sqrt{t})\cdot (V+a_3)\cdot (exp(\frac{a_4}{T})+I_0\cdot a_5(DOD + a_6)^2)$


## The Driving Cycle
The driving cycle is based of the Volkswagen ID. 4 Pro, as it has support for V2G, and was one of the most sold cars in Europe after its initial release. The driving is based on mild weather highway driving data, taken from EV-Database (https://ev-database.org/car/2028/Volkswagen-ID4-Pro). The range was during those conditions specified to be 400 KM. The discharge rate is therefore chosen to be $C = \frac{1}{4}$, which simplifies to 19.25 kW continous discharge based on the usable 77 kWh of capacity in the car. The driving cycle is initial choosen to continue during 4 hours, from 100% SOC to 0%, which means a DOD of 100%. This is assumed for the driving of both the cases.

In the python GUI, a custom C-value can be entered. But if you plan on modelling EV degradation, using the previously mentioned background as a starting point could be recommended.

## Calculating the DOD
Since the DOD will depend on the user input, the program looks at for how many consecutive hours the battery is discharging/charging, and combines this with the c-rate to adjust the DOD according to the cycling.