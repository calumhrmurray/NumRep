#!/usr/bin/python3
""" Two component decay Monte Carlo simulation

	This module contains a single class which can be used to run Monte Carlo simulations
	for a two component decay. This models the decay of a radioactive substance with two
	decay components.

"""

import scipy.optimize as optimize
import numpy as np

class distribution:
    """ Initialise distribution with f, tau1, tau2.
    	Perform observations or simulations with the def observation
    """
    
    # constructors
    def __init__(self, f, tau1, tau2):
        self.f = float(f)
        self.tau1 = float(tau1)
        self.tau2 = float(tau2)
        
    # method to return two component exponential decay distribution    
    def evaluate_d(self,t):
        return self.f*(1/self.tau1)*np.exp(-t/self.tau1)+(1-self.f)*(1/self.tau2)*np.exp(-t/self.tau2)
    
    # method to return maximum value of distribution  
    def maximum(self):
        # slightly larger than any value in the distribution for random number gen.
        # changing this number effects simulation results bias
        return self.evaluate_d(0)+0.0001
    
    # method to return random number with distribution
    def random_val(self,xlim=7.):           
        x1 = 0.
        x2 = 0.
        x3 = 1.
        while ( x3 > x2 ):
            x1 = np.random.uniform()
			# 7. is the largest decay time in the measurements used 
			# in this report 
            x1 = x1*xlim
            x2 = self.evaluate_d(x1)
            x3 = np.random.uniform() * self.maximum()
        
        return x1
    
    # integrates area under the curve, here normalised
    # therefore always roughly equal to 1
    def numeric_integral(self,lo,hi,npoints=100000):        
        sumf = 0        
        for i in range(0,npoints):
            x = lo+np.random.uniform()*(hi-lo)
            sumf += self.evaluate_d(x)            
        return sumf*(hi-lo)/npoints
    
    # negative log likelihood function
    def nll(self,theta,t):
        f,tau1,tau2 = theta
        return -np.sum(np.log(f*(1/tau1)*np.exp(-t/tau1)+(1-f)*(1/tau2)*np.exp(-t/tau2)))  
    
    # performs an observation by taking n_meas random values of the distribution
    def observation(self,n_meas=10000,method='TNC'):
        results = []
        for i in range(0,n_meas):
            results.append(self.random_val())
        # estimate the parameters by minimising nll
        mle_estimates = optimize.minimize(self.nll, [self.f, self.tau1, self.tau2],
					   args=(np.array(results)),method=method)
        # return estimated parameters, measurements
        return mle_estimates['x'], np.array(results)



