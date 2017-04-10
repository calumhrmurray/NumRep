import numpy as np
import tcdecay_distribution as tcd

test = tcd.distribution(0.74849409,  0.1978367 ,  1.30720393)

print('Running TNC simulations')

n = input('Enter number of decay particles: ')

results = []

for _ in range(500):
	results.append(test.observation(method='Nelder-mead',n_muons=int(n))[0])

print('Finished TNC simulations')

np.save('/home/calum/Documents/NumRep/max_likelihood/5run'+str(n)+'.npy',results)

