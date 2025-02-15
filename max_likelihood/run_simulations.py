import numpy as np
import tcdecay_distribution as tcd

test = tcd.distribution(0.74849409,  0.1978367 ,  1.30720393)

print('Running TNC simulations')

results = []
for _ in range(10000):
	results.append(test.observation()[0])

print('Finished TNC simulations')

np.save('/home/calum/Documents/NumRep/max_likelihood/large_run_sim_tnc.npy',results)


print('Running Nelder-mead simulations')

results = []

for _ in range(10000):
	results.append(test.observation(method='Nelder-mead')[0])

print('Finished Nelder-mead simulations')

np.save('/home/calum/Documents/NumRep/max_likelihood/large_run_sim_nm.npy',results)
	


