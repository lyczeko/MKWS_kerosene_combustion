
# coding: utf-8

# In[5]:


from SDToolbox import *
import cantera as ct

P1=1.4e+06
P1atm=P1/one_atm
T1=800
mix='NC10H22:1.0,O2:15.5,N2:58.28'
mech='JetSurf.cti'

[cj_speed,R2] = CJspeed(P1, T1, mix, mech, 0);   

gas = PostShock_eq(cj_speed, P1, T1, mix, mech)
Ps = gas.P/one_atm

print ' '
print 'CJ State'
gas()
Ps = gas.P/one_atm

print ' '
print 'For ' + mix + ' with P1 = %.2f atm & T1 = %.2f K using ' % (P1atm,T1) + mech 
print 'CJ Speed is %.2f m/s' % cj_speed

print 'The CJ State is %.2f atm & %.2f K' % (Ps,gas.T)

[ae,af] = equilSoundSpeeds(gas)

print 'The sound speeds are: af = %.2f m/s & ae = %.2f m/s' % (af,ae)
print ' '


# In[6]:


from SDToolbox import *
import cantera as ct

P1=1.4e+06
P1atm=P1/one_atm
T1=800
mix='NC10H22:1.0,O2:23.25,N2:87.42'
mech='JetSurf.cti'

[cj_speed,R2] = CJspeed(P1, T1, mix, mech, 0);   

gas = PostShock_eq(cj_speed, P1, T1, mix, mech)
Ps = gas.P/one_atm

print ' '
print 'CJ State'
gas()
Ps = gas.P/one_atm

print ' '
print 'For ' + mix + ' with P1 = %.2f atm & T1 = %.2f K using ' % (P1atm,T1) + mech 
print 'CJ Speed is %.2f m/s' % cj_speed

print 'The CJ State is %.2f atm & %.2f K' % (Ps,gas.T)

[ae,af] = equilSoundSpeeds(gas)

print 'The sound speeds are: af = %.2f m/s & ae = %.2f m/s' % (af,ae)
print ' '

