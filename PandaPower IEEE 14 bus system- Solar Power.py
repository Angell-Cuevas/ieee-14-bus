import pandapower as pp #We bring in the pandapower library (the main tool for power grid simulations) and give it a short nickname pp
import pandapower.networks as nw #This imports the built-in test networks part of pandapower, nicknamed nw. It contains ready-made grid models like the IEEE 14-bus system.
import matplotlib.pyplot as plt #Imports the plotting part of matplotlib (the standard Python graphing library), nicknamed plt
import pandapower.plotting as plot #Imports pandapower's own plotting tools, nicknamed plot


net = nw.case14() #Creates a variable called net (short for network) and loads the standard IEEE 14-bus test system into it

#net.bus.vn_kv = net.bus.vn_kv / 10  # Roughly scales to medium voltage
#initially tried to decresed bus values by 10 but did not work. so then used code shown below instead

# NEW: Smaller solar to help convergence
pp.create_sgen(net, bus=9, p_mw=-1.5, q_mvar=0, name="Solar at Bus 9") #Creates a static generator (sgen = solar, wind, batteries, etc.) connected to bus 9.
# Negative power means it's injecting 1.5 MW into the grid (positive would mean consuming) #No reactive power (solar inverters often run at unity power factor)
pp.create_sgen(net, bus=10, p_mw=-1.0, q_mvar=0, name="Solar at Bus 10") #Creates a static generator connected to bus 10 that injects 1.0 MW of power named Solar at Bus 10
pp.create_sgen(net, bus=13, p_mw=-2.0, q_mvar=0, name="Solar at Bus 13") #Creates a static generator connected to bus 13 that injects 2.0 MW of power named Solar at Bus 13

# Run power flow with fixes
pp.runpp(net, numba=False, max_iteration=20)  # Runs Powerpanda power flow calculation, no warning about numba when equal to false, max iterations of 20

# Scale loads and generators down (distribution has smaller MW)
net.load.p_mw = net.load.p_mw / 5 #Reduces active power (real power in MW) of all loads by dividing by 5.
net.load.q_mvar = net.load.q_mvar / 5 #Reduces reactive power (in MVAR) of loads by 5.
net.gen.p_mw = net.gen.p_mw / 5 #Reduces power output of traditional generators by 5.
net.ext_grid.vm_pu = 1.05  # Substation voltage a bit higher, This helps keep voltages stable when we add solar

# Results comparison
print("BASE CASE LOSSES (no solar): ~13.59 MW (original scale)")
print(f"WITH SOLAR LOSSES: {net.res_line.pl_mw.sum():.2f} MW") #Calculates and prints total active power losses in all lines (.sum() adds them up, :.2f = 2 decimal places).
print("Notice: Losses should drop because solar generates power closer to loads!") 

# Plots (updated)
plot.simple_plot(net, show_plot=True) #Draws a simple map of the entire grid (buses as dots, lines connecting them) and pops it up in a window

net.res_bus.vm_pu.plot(kind='bar', title='Voltage Profile WITH Solar (pu)') #Takes the calculated voltage results (res_bus.vm_pu) and makes a bar chart.
plt.savefig('voltages_with_solar.png')
plt.show()

net.res_line.loading_percent.plot(kind='bar', title='Line Loading WITH Solar (%)') 
plt.savefig('loading_with_solar.png')
plt.show()

# OUTPUT:
#BASE CASE LOSSES (no solar): ~13.59 MW (original scale)
#WITH SOLAR LOSSES: 13.96 MW
#Notice: Losses should drop because solar generates power closer to loads!
# + Chart and Graphs
