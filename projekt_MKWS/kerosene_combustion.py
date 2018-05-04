
# coding: utf-8

# In[86]:


get_ipython().run_line_magic('matplotlib', 'inline')

import sys
import os
import math
import csv
import numpy as np

import cantera as ct

#combustion chamber volume and mass flows assesment based on the dimensions of Rolls Royce AE3007

lambda_air = 1.5 #air–fuel equivalence ratio

air = ct.Solution('air.cti')
air.TP = 800, 1.4e+06 #typical temperature and pressure behind HPC
air_in=ct.Reservoir(air)
air_mdot=ct.Quantity(air, mass=20)

fuel = ct.Solution('Dagaut_Ori.cti')
fuel.TPY = 300, 3e+05, 'NC10H22:0.74,PHC3H7:0.15,CYC9H18:0.11'
fuel_in=ct.Reservoir(fuel)
fuel_mdot = ct.Quantity(fuel, mass=1)
fuel_mdot.mass=air_mdot.mass/lambda_air/14.9

#igniter (like in "combustor.py")
fuel.TPX = 1500, 2e+06, 'H:1.0'
igniter = ct.Reservoir(fuel)

fuel.TPX = 1100, 1.2e+6, 'N2:1.0' #combustion chamber already hot, otherwise some mechanims doesn't integrate properly when combustor temperature is below 1000 K
combustor = ct.IdealGasReactor(fuel, energy='on')
combustor.volume = 0.2

#exhaust reservoir
fuel.TPX = 300, ct.one_atm, 'N2:1.0'
exhaust = ct.Reservoir(fuel)

m1 = ct.MassFlowController(fuel_in, combustor, mdot=fuel_mdot.mass)
m2 = ct.MassFlowController(air_in, combustor, mdot=air_mdot.mass)

fwhm = 0.01
amplitude = 0.1
t0 = 0.2
igniter_mdot = lambda t: amplitude * math.exp(-(t-t0)**2 * 4 * math.log(2) / fwhm**2)
m3 = ct.MassFlowController(igniter, combustor, mdot=igniter_mdot)

v = ct.Valve(combustor, exhaust, K=1)

sim = ct.ReactorNet([combustor])

time=0.0
Tprev = combustor.T
states = ct.SolutionArray(fuel, extra=['t','tres'])

for n in range (5000):
    time +=0.0002
    sim.advance(time)
    tres = combustor.mass/v.mdot(time)
    Tnow = combustor.T
    states.append(fuel.state, t=time, tres=tres)

states.write_csv('combustor.csv', cols=('t','T','P','X'))
print(combustor.thermo.report())

import matplotlib.pyplot as plt
plt.figure()
plt.plot(states.t, states.T)
plt.xlabel('Time [s]')
plt.ylabel('Temperature [K]')
plt.title('Temperature')
plt.savefig('T.pdf')
plt.show()

plt.figure()
plt.plot(states.t, states.P)
plt.xlabel('Time [s]')
plt.ylabel('Pressure [Pa]')
plt.ticklabel_format(style='sci', axis='y', scilimits=(0,0))
plt.tight_layout()
plt.title('Pressure')
plt.savefig('P.pdf')
plt.show()

