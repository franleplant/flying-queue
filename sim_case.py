import parts

sys = parts.System([1,2], [1,4], 1000, 1)

results = sys.run_simulation()

print('Lq_mean:', results['Lq_mean'])
print('Ls_mean:', results['Ls_mean'])
print('Wq_mean:', results['Wq_mean'])
print('Ws_mean:', results['Ws_mean'])
print('Cm_mean:', results['Cm_mean'])