clc
clear variables

% Based on a Volkswagen ID. 4, from EV-database. C-rate of 1/4 for both
% discharging and charging (19.25 kW). 

% Driving based on 23 Celsius, 110 km/h 
T = 23+273.15;
Voltage = 3.6; % Assume Nominal voltage
I_0 = 3; % [Assuming cell-level, with 12 Ah cells


% SOC of the different drive cycles throughout a day
% These are all not used in this version however, but as driving cycles changes
% they will likely become useful
BD_excessive_dailycycle = [0.5, 0.75, 0.5, 0.75, 0.5, 0.75, 0.5, 0.75, 1.0, 0.75, 0.5, 0.25, 0, 0.25, 0.5, 0.75, 0.5, 0.75, 0.5, 0.75, 0.5, 0.75, 0.5, 0.75];
no_BD_dailycycle = [1, 1, 1, 1, 1, 1, 1, 1, 1, 0.75, 0.5, 0.25, 0, 0.25, 0.5, 0.75, 1, 1, 1, 1, 1, 1, 1, 1];
no_BD_power = [0, 0, 0, 0, 0, 0, 0, 0, 19.25, 19.25, 19.25, 19.25, 19.25, 19.25, 19.25, 19.25, 0, 0, 0, 0, 0, 0, 0, 0];
BD_DOD = 0.5; % Average, approx 2 cycles with 25% and one with 100%
no_BD_DOD = 1;
no_BD_SOC = 1;


C_rate = 1/4; % Same during charge and discharge
power = 19.25 * 10^3; % [W]

sim_days = 30; % Number of days to simulate battery tear
% OBSERVE: Inaccurate on small number of days, as the linear model of the
% calendar agings +1-term becomes to significant.

BD_excessive_cycle = repmat(BD_excessive_dailycycle, 1, sim_days);
no_BD_cycle = repmat(no_BD_dailycycle, 1, sim_days);
no_BD_power = repmat(no_BD_power, 1, sim_days);

% Cycling model used from SPM
% Fitting Parameters
a1 = 4.34*10^(-7);
a2 = 35;
a3 = -3.23;
a4 = -5010;
a5 = 0.64;
a6 = 63.7;

t = linspace(1, length(BD_excessive_cycle), length(BD_excessive_cycle));

%% MODEL FOR CONSTANTLY USED EV
% Since BD is constantly cycling, we do not need to use the calendar aging
% model
C_loss_bd = a1*(t+a2*sqrt(t))*(Voltage+a3)*(exp(a4/T)+I_0*a5*(BD_DOD+a6)^2); 




%% MODEL FOR CALENDAR + CYCLIC
% Calendar model for 45 celsius used, as the temperature is likely higher in the
% battery pack then the ambient. The model is also understated compared
% with others


C_loss_no_bd_warm = ones(1, length(no_BD_cycle));
C_loss_no_bd_cold = ones(1, length(no_BD_cycle));
func_value_warm = 1+(0.004*no_BD_SOC)*t(1); % Initial Value, first hour is assumed to be idle
func_value_cold = (0.09*no_BD_SOC+0.01)*sqrt(t(1)); % Initial Value, first hour is assumed to be idle

C_loss_no_bd_warm(1) = func_value_warm;
C_loss_no_bd_cold(1) = func_value_cold;
for i=2:length(no_BD_power)
    if no_BD_power(i)==0 % Use Calendar aging model
        %C_loss_no_bd(i) = 1+(0.004*no_BD_SOC)*t(i);
            
        % Warm ambient temperature
        C_loss_no_bd_warm(i) = func_value_warm + 0.004*no_BD_SOC; % Eulers Method, 45 deg
        func_value_warm = C_loss_no_bd_warm(i);            
        
        % Cold ambient temperature
        C_loss_no_bd_cold(i) = func_value_cold + (0.045*no_BD_SOC+0.005)/(sqrt(t(i))); % Eulers Method
        func_value_cold = C_loss_no_bd_cold(i);
    else
        % C_loss_no_bd(i) = a1*(t(i)+a2*sqrt(t(i)))*(Voltage+a3)*(exp(a4/T)+I_0*a5*(no_BD_DOD+a6)^2);
        C_loss_no_bd_cold(i) = func_value_cold + a1*(a2/(2*sqrt(t(i)))+1)*(a3+Voltage)*(exp(a4/T)+a5*I_0*(a6+no_BD_DOD)^2);
        C_loss_no_bd_warm(i) = func_value_warm + a1*(a2/(2*sqrt(t(i)))+1)*(a3+Voltage)*(exp(a4/T)+a5*I_0*(a6+no_BD_DOD)^2);
        func_value_cold = C_loss_no_bd_cold(i);
        func_value_warm = C_loss_no_bd_warm(i);
    end
end

subplot(2, 1, 1)
plot(t, C_loss_bd, "linewidth", 2, "LineStyle","-", "color", "r")
title("BD-Charging Application (0% Idle Battery)", "FontSize", 14, "FontWeight", "normal", "FontName", "Times New Roman")
ylabel("Capacity Loss [%]")
xlabel("Time [h]")

subplot(2, 1, 2)
plot(t, C_loss_no_bd_warm, "linewidth", 2, "LineStyle","-", "color", "r")
hold on
plot(t, C_loss_no_bd_cold, "linewidth", 2, "LineStyle","-", "color", "b")
title("No BD-Charging, SOC at 100%, 67% Idle Time", "FontSize", 14, "FontWeight", "normal", "FontName", "Times New Roman")
ylabel("Capacity Loss [%]")
xlabel("Time [h]")

legend("Idleing ambient temp: 45C", "Idleing ambient temp. -5C")
