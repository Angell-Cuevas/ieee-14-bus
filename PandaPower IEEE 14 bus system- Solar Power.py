import pandapower as pp
import pandapower.networks as nw
import matplotlib.pyplot as plt
import pandapower.plotting as plot


net = nw.case14()


# NEW: Make it more distribution-like
# Scale all bus voltages down (distribution level ~12-33 kV base)

#net.bus.vn_kv = net.bus.vn_kv / 10  # Roughly scales to medium voltage
#initially tried to decresed bus values by 10 but did not work. so then used code shown below instead

# NEW: Smaller solar to help convergence
pp.create_sgen(net, bus=9, p_mw=-1.5, q_mvar=0, name="Solar at Bus 9")
pp.create_sgen(net, bus=10, p_mw=-1.0, q_mvar=0, name="Solar at Bus 10")
pp.create_sgen(net, bus=13, p_mw=-2.0, q_mvar=0, name="Solar at Bus 13")

# Run power flow with fixes
pp.runpp(net, numba=False, max_iteration=20)  # More tries, no warning

# Scale loads and generators down (distribution has smaller MW)
net.load.p_mw = net.load.p_mw / 5
net.load.q_mvar = net.load.q_mvar / 5
net.gen.p_mw = net.gen.p_mw / 5
net.ext_grid.vm_pu = 1.05  # Substation voltage a bit higher

# NEW: Add distributed solar PV (as "sgen" = static generator)
# Example: Add 3 MW solar at bus 9, 2 MW at bus 10, 4 MW at bus 13 (negative P for injection)
pp.create_sgen(net, bus=9, p_mw=-3.0, q_mvar=0, name="Solar at Bus 9")
pp.create_sgen(net, bus=10, p_mw=-2.0, q_mvar=0, name="Solar at Bus 10")
pp.create_sgen(net, bus=13, p_mw=-4.0, q_mvar=0, name="Solar at Bus 13")

# Run power flow again
pp.runpp(net)

# Results comparison
print("BASE CASE LOSSES (no solar): ~13.59 MW (original scale)")
print(f"WITH SOLAR LOSSES: {net.res_line.pl_mw.sum():.2f} MW")
print("Notice: Losses should drop because solar generates power closer to loads!")

# Plots (updated)
plot.simple_plot(net, show_plot=True)

net.res_bus.vm_pu.plot(kind='bar', title='Voltage Profile WITH Solar (pu)')
plt.savefig('voltages_with_solar.png')
plt.show()

net.res_line.loading_percent.plot(kind='bar', title='Line Loading WITH Solar (%)')
plt.savefig('loading_with_solar.png')
plt.show()

