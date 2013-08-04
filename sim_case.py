import sim

sys = sim.System([1,2], [1,3], 20, 1)
results = sys.run_simulation()
sys.print_results()

