import numpy as np
import matplotlib.pyplot as plt
# import gui as g

#! MODEL PARAMETERS
# Cycling model used from SPM
# Fitting Parameters
a1 = 4.34*10**(-7);
a2 = 35;
a3 = -3.23;
a4 = -5010;
a5 = 0.64;
a6 = 63.7;

Voltage = 3.7
T = 273.15+25 # Assuming 25 degrees celsius


def calc_deg(daily_soc, daily_soc2, sim_days, global_status_list1, global_status_list2, c_rate):

    # sim_days = int(g.sim_days_entry.get())

    I_0 = 12*float(c_rate) # Current of the 12 Ah battery


    soc = np.tile(daily_soc, sim_days)
    status_cycle_1 = np.tile(global_status_list1, sim_days)
    dod = []


    i = 0
    while len(dod)<len(status_cycle_1):
        if status_cycle_1[i] == 2: # The car is idle
            dod.append(0) # The DOD is zero if the battery is not charging. This will indicate a switch of mathematical model
            i += 1
        elif status_cycle_1[i] == 1:
            j = 1
            cur_dod = float(c_rate)*100
            while status_cycle_1[i+j] == 1:
                cur_dod += float(c_rate) * 100
                j += 1
            dod.extend([cur_dod] * j)
            i = i + j
        elif status_cycle_1[i] == 0: # The same as before, but for charging instead.
            j = 1
            cur_dod = float(c_rate)*100
            while status_cycle_1[i+j] == 0:
                cur_dod += float(c_rate)*100
                j += 1
            dod.extend([cur_dod] * j)
            i = i+j


    deg = []
    
    # Initial value, cold calendar aging
    t = np.linspace(0, sim_days*24, sim_days*24)
    val = (0.09*soc[0]/100+0.01)*np.sqrt(t[0]);
    deg.append(val)
    for d in range(1, len(dod)):
        if dod[d] == 0: # The battery is idle
            deg.append(val+(0.045*soc[d]/100+0.005)/(np.sqrt(t[d])))
        else: # Battery is Cycling
            deg.append(val+a1*(a2/(2*np.sqrt(t[d]))+1)*(a3+Voltage)*(np.exp(a4/T)+a5*I_0*(a6+dod[d]/100)**(2)))
        val = deg[-1]
    
    plt.subplot(2, 1, 1)
    plt.plot(t, deg)
    plt.title(f"Cycle 1 Degredation")


    ## CYCLE 2 ##
    soc2 = np.tile(daily_soc2, sim_days)
    status_cycle_2 = np.tile(global_status_list2, sim_days)
    dod = []


    i = 0
    while len(dod)<len(status_cycle_2):
        if status_cycle_2[i] == 2: # The car is idle
            dod.append(0) # The DOD is zero if the battery is not charging. This will indicate a switch of mathematical model
            i += 1
        elif status_cycle_2[i] == 1:
            j = 1
            cur_dod = float(c_rate)*100
            while status_cycle_2[i+j] == 1:
                cur_dod += float(c_rate) * 100
                j += 1
            dod.extend([cur_dod] * j)
            i = i + j
        elif status_cycle_2[i] == 0: # The same as before, but for charging instead.
            j = 1
            cur_dod = float(c_rate)*100
            while status_cycle_1[i+j] == 0:
                cur_dod += float(c_rate)*100
                j += 1
            dod.extend([cur_dod] * j)
            i = i+j


    deg2 = []
    
    # Initial value, cold calendar aging
    t = np.linspace(0, sim_days*24, sim_days*24)
    val = (0.09*soc2[0]/100+0.01)*np.sqrt(t[0]);
    deg2.append(val)
    for d in range(1, len(dod)):
        if dod[d] == 0: # The battery is idle
            deg2.append(val+(0.045*soc2[d]/100+0.005)/(np.sqrt(t[d])))
        else: # Battery is Cycling
            deg2.append(val+a1*(a2/(2*np.sqrt(t[d]))+1)*(a3+Voltage)*(np.exp(a4/T)+a5*I_0*(a6+dod[d]/100)**(2)))
        val = deg2[-1]
    
    plt.subplot(2, 1, 2)
    plt.plot(t, deg2)
    plt.title(f"Cycle 2 Degredation")

    plt.show()