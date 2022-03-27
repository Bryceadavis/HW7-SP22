from Steam_work import steam
import numpy as np
from matplotlib import pyplot as plt
#All code here is from Dr.Smay's Rankine.py file for EX2 except for import alteration in line 1

class rankine():
    def __init__(self, p_low=8, p_high=8000, t_high=None, eff_turbine=1.0, name='Rankine Cycle'):
        '''
        Constructor for rankine power cycle.  If t_high is not specified, the State 1
        is assigned x=1 (saturated steam @ p_high).  Otherwise, use t_high to find State 1.
        :param p_low: the low pressure isobar for the cycle in kPa
        :param p_high: the high pressure isobar for the cycle in kPa
        :param t_high: optional temperature for State1 (turbine inlet) in degrees C
        :param eff_turbine: isentropic efficiency of the turbine
        :param name: a convenient name
        '''
        self.p_low=p_low
        self.p_high=p_high
        self.t_high=t_high
        self.name=name
        self.efficiency=None
        self.turbine_eff=eff_turbine
        self.turbine_work=0
        self.pump_work=0
        self.heat_added=0
        self.state1=None
        self.state2s=None
        self.state2=None
        self.state3=None
        self.state4=None

    def calc_efficiency(self):
        #calculate the 4 states
        #state 1: turbine inlet (p_high, t_high) superheated or saturated vapor
        if(self.t_high==None):
            self.state1 = steam(self.p_high, x=1.0, name='Turbine Inlet') # instantiate a steam object with conditions of state 1 as saturated steam, named 'Turbine Inlet'
        else:
            self.state1= steam(self.p_high,T=self.t_high,name='Turbine Inlet') # instantiate a steam object with conditions of state 1 at t_high, named 'Turbine Inlet'
        #state 2: turbine exit (p_low, s=s_turbine inlet) two-phase
        self.state2s = steam(self.p_low, s=self.state1.s, name="Turbine Exit")  # instantiate a steam object with conditions of state 2s, named 'Turbine Exit'
        if self.turbine_eff <1.0:  # eff=(h1-h2)/(h1-h2s) -> h2=h1-eff(h1-h2s)
            h2=self.state1.h-self.turbine_eff*(self.state1.h-self.state2s.h)
            self.state2=steam(self.p_low,h=h2, name="Turbine Exit")
        else:
            self.state2=self.state2s
        #state 3: pump inlet (p_low, x=0) saturated liquid
        self.state3= steam(self.p_low,x=0, name='Pump Inlet') # instantiate a steam object with conditions of state 3 as saturated liquid, named 'Pump Inlet'
        #state 4: pump exit (p_high,s=s_pump_inlet) typically sub-cooled, but estimate as saturated liquid
        self.state4=steam(self.p_high,s=self.state3.s, name='Pump Exit')
        self.state4.h=self.state3.h+self.state3.v*(100*self.p_high-100*self.p_low)

        self.turbine_work= self.state1.h - self.state2.h # calculate turbine work
        self.pump_work= self.state4.h - self.state3.h # calculate pump work
        self.heat_added= self.state1.h - self.state4.h # calculate heat added
        self.efficiency=100.0*(self.turbine_work - self.pump_work)/self.heat_added
        return self.efficiency

    def print_summary(self):

        if self.efficiency==None:
            self.calc_efficiency()
        print('Cycle Summary for: ', self.name)
        print('\tEfficiency: {:0.3f}%'.format(self.efficiency))
        print('\tTurbine Eff:  {:0.2f}'.format(self.turbine_eff))
        print('\tTurbine Work: {:0.3f} kJ/kg'.format(self.turbine_work))
        print('\tPump Work: {:0.3f} kJ/kg'.format(self.pump_work))
        print('\tHeat Added: {:0.3f} kJ/kg'.format(self.heat_added))
        self.state1.print()
        self.state2.print()
        self.state3.print()
        self.state4.print()

    def plot_cycle_TS(self):
        """
        I want to plot the Rankine cycle on T-S coordinates along with the vapor dome and shading in the cycle.
        I notice there are several lines on the plot:
        saturated liquid T(s) colored blue
        saturated vapor T(s) colored red
        The high and low isobars and lines connecting state 1 to 2, and 3 to saturated liquid at phigh
        step 1:  build data for saturated liquid line
        step 2:  build data for saturated vapor line
        step 3:  build data between state 3 and sat liquid at p_high
        step 4:  build data between sat liquid at p_high and state 1
        step 5:  build data between state 1 and state 2
        step 6:  build data between state 2 and state 3
        step 7:  put together data from 3,4,5 for top line and build bottom line
        step 8:  make and decorate plot
        :return:
        """
        #step 1&2:
        ts, ps, hfs, hgs, sfs, sgs, vfs, vgs= np.loadtxt('sat_water_table.txt',skiprows=1, unpack=True) #use np.loadtxt to read the saturated properties
        plt.plot(sfs,ts, color='blue')
        plt.plot(sgs, ts, color='red')

        #step 3:  I'll just make a straight line between state3 and state3p
        st3p=steam(self.p_high,x=0) #saturated liquid state at p_high
        svals=np.linspace(self.state3.s, st3p.s, 20)
        tvals=np.linspace(self.state3.T, st3p.T, 20)
        line3=np.column_stack([svals, tvals])
        #plt.plot(line3[:,0], line3[:,1])

        #step 4:
        sat_pHigh=steam(self.p_high, x=1.0)
        st1=self.state1
        svals2p=np.linspace(st3p.s, sat_pHigh.s, 20)
        tvals2p=[st3p.T for i in range(20)]
        line4=np.column_stack([svals2p, tvals2p])
        if st1.T>sat_pHigh.T:  #need to add data points to state1 for superheated
            svals_sh=np.linspace(sat_pHigh.s,st1.s, 20)
            tvals_sh=np.array([steam(self.p_high,s=ss).T for ss in svals_sh])
            line4 =np.append(line4, np.column_stack([svals_sh, tvals_sh]), axis=0)
        #plt.plot(line4[:,0], line4[:,1])

        #step 5:
        svals=np.linspace(self.state1.s, self.state2.s, 20)
        tvals=np.linspace(self.state1.T, self.state2.T, 20)
        line5=np.array(svals)
        line5=np.column_stack([line5, tvals])
        #plt.plot(line5[:,0], line5[:,1])

        #step 6:
        svals=np.linspace(self.state2.s, self.state3.s, 20)
        tvals=np.array([self.state2.T for i in range(20)])
        line6=np.column_stack([svals, tvals])
        #plt.plot(line6[:,0], line6[:,1])

        #step 7:
        topLine=np.append(line3, line4, axis=0)
        topLine=np.append(topLine, line5, axis=0)
        xvals=topLine[:,0]
        y1=topLine[:,1]
        y2=[self.state3.T for s in xvals]

        plt.plot(xvals, y1, color='darkgreen')
        plt.plot(xvals, y2, color='black')
        plt.fill_between(xvals, y1, y2, color='gray', alpha=0.5)
        plt.plot(self.state1.s, self.state1.T, marker='o', markeredgecolor='k', markerfacecolor='w')
        plt.plot(self.state2.s, self.state2.T, marker='o', markeredgecolor='k', markerfacecolor='w')
        plt.plot(self.state3.s, self.state3.T, marker='o', markeredgecolor='k', markerfacecolor='w')
        plt.xlabel(r's $\left(\frac{kJ}{kg\cdot K}\right)$')
        plt.ylabel(r'T $\left( ^{o}C \right)$')
        plt.title(self.name)

        sMin=min(sfs)
        sMax=max(sgs)
        plt.xlim(sMin, sMax)

        tMin=min(ts)
        tMax=max(max(ts),st1.T)
        plt.ylim(tMin,tMax*1.05)

        txt= 'Summary:'
        txt+= '\n$\eta_{cycle} = $'+'{:0.2f}%'.format(self.efficiency)
        txt+= '\n$\eta_{turbine} = $'+'{:0.2f}'.format(self.turbine_eff)
        txt+= '\n$W_{turbine} = $'+ '{:0.2f}'.format(self.turbine_work)+r'$\frac{kJ}{kg}$'
        txt+= '\n$W_{pump} = $'+'{:0.2f}'.format(self.pump_work)+r'$\frac{kJ}{kg}$'
        txt+= '\n$Q_{in} = $'+ '{:0.2f}'.format(self.heat_added)+r'$\frac{kJ}{kg}$'
        plt.text(sMin+0.05*(sMax-sMin), tMax, txt, ha='left', va='top')

        plt.show()

def main():
    rankine1= rankine(8,8000,t_high=500,eff_turbine=1.0, name='Rankine Cycle - Superheated at turbine inlet') #instantiate a rankine object to test it.
    #t_high is specified
    #if t_high were not specified, then x_high = 1 is assumed
    eff=rankine1.calc_efficiency()
    print(eff)
    rankine1.print_summary()
    rankine1.plot_cycle_TS()

if __name__=="__main__":
    main()