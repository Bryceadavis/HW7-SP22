import numpy as np

from Steam_work import steam
import matplotlib.pyplot as plt

class rankine():
    def __init__(self, p_low=8, p_high=8000, eff_turbine=0.95, t_high=None, name='Rankine Cycle'):
        '''
        Constructor for rankine power cycle.  If t_high is not specified, the State 1
        is assigned x=1 (saturated steam @ p_high).  Otherwise, use t_high to find State 1.
        :param p_low: the low pressure isobar for the cycle in kPa
        :param p_high: the high pressure isobar for the cycle in kPa
        :param t_high: optional temperature for State1 (turbine inlet) in degrees C
        :param name: a convenient name
        '''
        self.p_low=p_low
        self.p_high=p_high
        self.t_high=t_high
        self.name=name
        self.efficiency=None
        self.turbine_work=0
        self.pump_work=0
        self.heat_added=0
        self.state1=None
        self.state2=None
        self.state3=None
        self.state4=None
        self.eff_turbine=eff_turbine # Rankine class modified to include a value for isentropic turbine efficiency

    def calc_efficiency(self):
        #calculate the 4 states
        #state 1: turbine inlet (p_high, t_high) superheated or saturated vapor
        if(self.t_high==None):
            self.state1 = steam(self.p_high, x=1.0, name='Turbine Inlet') # instantiate a steam object with conditions of state 1 as saturated steam, named 'Turbine Inlet'
        else:
            self.state1= steam(self.p_high, T=self.t_high, name='Turbine Inlet') # instantiate a steam object with conditions of state 1 at t_high, named 'Turbine Inlet'
        #state 2: turbine exit (p_low, s=s_turbine inlet) two-phase
        self.state2= steam(self.p_low, s=self.state1.s, name="Turbine Exit") # instantiate a steam object with conditions of state 2, named 'Turbine Exit'
        #state 3: pump inlet (p_low, x=0) saturated liquid
        self.state3= steam(self.p_low, x=0, name='Pump Inlet') # instantiate a steam object with conditions of state 3 as saturated liquid, named 'Pump Inlet'
        #state 4: pump exit (p_high,s=s_pump_inlet) typically sub-cooled, but estimate as saturated liquid
        self.state4=steam(self.p_high, s=self.state3.s, name='Pump Exit')
        self.state4.h=self.state3.h+self.state3.v*(self.p_high*100-self.p_low*100)

        self.turbine_work= (self.state1.h - self.state2.h)*self.eff_turbine # calculate turbine work #multiplied by turbine efficiency
        self.pump_work= self.state4.h - self.state3.h # calculate pump work
        self.heat_added= (self.state1.h - self.state4.h) # calculate heat added
        self.efficiency=100.0*(self.turbine_work - self.pump_work)/self.heat_added
        return self.efficiency

    def print_summary(self):

        if self.efficiency==None:
            self.calc_efficiency()
        print('Cycle Summary for: ', self.name)
        print('\tEfficiency: {:0.3f}%'.format(self.efficiency))
        print('\tTurbine Work: {:0.3f} kJ/kg'.format(self.turbine_work))
        print('\tPump Work: {:0.3f} kJ/kg'.format(self.pump_work))
        print('\tHeat Added: {:0.3f} kJ/kg'.format(self.heat_added))
        self.state1.print()
        self.state2.print()
        self.state3.print()
        self.state4.print()

    def plot_cycle_TS(self):
        """
        This function will graph the rankine cycle from HW6 part 3 on a T-S diagram.
        The two halves of the main curve,SaturatedLiquidLine and SaturatedVaporLine, are from sat_water_table.txt file.
        Graph also includes isobars for plow and phigh (constructed from state objects above and steam objects in Steam_work.py).
        :return: none, just the graph
        """
        ts, ps, hfs, hgs, sfs, sgs, vfs, vgs = np.loadtxt('sat_water_table.txt', skiprows=1, unpack=True) #reads values from water table txt file
        #tcol, hcol, scol, pcol = np.loadtxt('superheated_water_table.txt', skiprows=1, unpack=True)
        plt.xlim(0,8.99) #sets limits on x
        plt.ylim(0,550) #sets limits on y
        plt.plot(sfs,ts) #plots the sat fluid entropy vs. Tsat
        plt.plot(sgs,ts,color='red') #plots the sat vapor entropy vs. Tsat #resposible for the right half of the curve
        x1vals=[self.state3.s,self.state2.s]
        y1vals=[self.state3.T,self.state2.T]
        plt.plot(x1vals,y1vals, color='black') #plots the plow isobar
        xs=steam(8000,x=0) #these 4 lines are the 2 points near the vapor dome
        p1,p2=xs.s,xs.T
        xt=steam(8000,x=1)
        p3,p4=xt.s,xt.T
        x2vals=[self.state3.s,p1,p3,self.state1.s,self.state2.s] #x vals for green curve
        y2vals=[self.state3.T,p2,p4,self.state1.T,self.state2.T] #y vals for green curve
        #print(self.state1.s)
        plt.plot(x2vals,y2vals, color='green') #plots the phigh isobar
        plt.fill_between(x2vals,y2vals,self.state2.T,facecolor='gray',alpha=0.15) #fills in the graph between phigh and plow isobars
        plt.xlabel(r'S $\left(\frac{kJ}{{kg\cdot K}}\right)$', fontsize=12) #xlabel
        plt.ylabel(r'T $\left(^o C\right)$', fontsize=12) #ylabel
        plt.text(0.5,380,'Summary:\n$\eta$: {:0.1f}%\n$\eta_{}:$ {:0.2f}\n$W_{}$: {:0.1f} kJ/kg\n$W_{}$: {:0.1f} kJ/kg\n$Q_{}$: {:0.1f} kJ/kg'
                 .format(self.efficiency,'{turbine}',self.eff_turbine,"{turbine}",self.turbine_work,"{pump}",self.pump_work,"{boiler}",self.heat_added))
        #this Summary was so fun to figure out how to write....turns out you need those brackets around the string in the format section...
        #unless you only want the first letter to be subscripted...*pterodactyl screech*
        plt.plot(self.state1.s,self.state1.T,marker='o', markerfacecolor='white', markeredgecolor='black', markersize=6) #state markers
        plt.plot(self.state2.s,self.state2.T,marker='o', markerfacecolor='white', markeredgecolor='black', markersize=6)
        plt.plot(self.state3.s,self.state3.T,marker='o', markerfacecolor='white', markeredgecolor='black', markersize=6)
        plt.title(self.name)
        plt.show()
        pass

def main(): # This doesn't run for Q3 of the exam so I initially fed it values to check the numbers for my summary
    rankine1= rankine(8,8000,t_high=500,eff_turbine=0.95,name='Rankine Cycle - Superheated at turbine inlet') #instantiate a rankine object to test it.
    #t_high is specified
    #if t_high were not specified, then x_high = 1 is assumed
    eff=rankine1.calc_efficiency()
    print(eff)
    rankine1.print_summary()
    rankine1.plot_cycle_TS()

if __name__=="__main__":
    main()
