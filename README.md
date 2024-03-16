# Introduction
It is well known that Litium-Ion batteries degrades over time. This behaviour is however been proven to be hard to model, both due to each batteries individual properties, and also since the degradation depends on many types of factors, such as discharge rates, ambient Temperature, Depth of Discharge (DOD), State of Charge (SOC) when idle, time and Voltage.

However, the degradation can generally be divided into calendar aging and cyclic aging. Calendar aging depends mainly on the SOC the battery is left in, and ambient temperature, whereas the cyclic aging depends on the Discharge rate, (or C-rate), Voltage and the DOD. 

This Model investigates the battery tear of a specific daily use, with the main objecting to investigate how Bi-Directional Charging Applications, such as Vehicles-to-Grid (V2G) and Vehicles-to-Home (V2H) will effect the aging, compared to leaving the battery at a certain SOC in either a -5 Degree Celsius environment, or a 45 Degree Celsius environment.

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

# MATLAB
The MATLAB cycle file allows for manual use of the empirical formulas. By creating a driving cycle matrix based on SOC and a given c-rate, the aging is calculated. Use at least 20 days in order for the model to be accurate.

# Python GUI Lab Environment
I am currently working on a GUI which makes the testing more intuitive. It has a few dependencies and is not yet completed. Currently the only thing completed are the SOC calculations and the first version of the interface.

### Dependencies
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


### How to use
Run the program from an IDE or the terminal, from the base directory as follows
```shell script
python3 python_gui/gui.py
```

The program asks to input at "Base SOC". This is used both as the initial state of charge in the daily cycle, but also to calculate the Depth of Discharge (DOD), which is an important factor i cyclic aging. An electric car, generally does not charge above 80%, which makes it a good base SOC.

The c-rate, or discharge rate is set to 1/5 initially. This also depends on application, but you will rarely discharge an electric car at a higher c-rate than 1/4, as mentioned in the background of the driving cycle.

# About
## Contributions
Created by Axel Nilsson as part of the Bachelor Thesis Bi-Directional charging, which consists of 4 other students at Chalmers University of Technology, and 5 students from Penn-State University.

## Planned Updates
I am currently investigating other models in order to not having to implement two different models that are made after different cell chemistries (NMC and LFP).

The GUI is not functioning yet. Since it is not a necessary part of the Thesis, it will be updated somewhat unregulary.