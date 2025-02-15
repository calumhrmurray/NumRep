import matplotlib.pyplot as plt
import numpy as np
import math

def find_t(array,t):
    array = np.array([row[1] for row in array])
    return (np.abs(array-t)).argmin()

# ODE classes

# electric field dE(x)/dx = rho(x)
class ode_electric_field:
    def __init__(self,height):
        print('Creating ODE: electric field')
        self.height = height
        self.initial = [0.,0.]
        
    def first_derivative(self,pair):
        if pair[1] < 1. :
            return 0.
        elif pair[1] < 2. :
            return 1. * self.height
        elif pair[1] < 3. :
            return -1 * self.height
        else :
            return 0.
        
    def initial_val(self):
        return self.initial
    
    # unknown
    def exact_solution(self,t):
        if t < 1.:
            return 0.
        elif t < 2.:
            return t-1
        elif t < 3.:
            return 3-t
        else:
            return 0 
        
# voltage dV(x)/dx = -E(x)
class ode_voltage:
    # method term decides whether to use discrete data from previous calculation or analytic version
    def __init__(self,method='discrete'):
        self.initial = [0.,0.]
        self.method = method
        self.E = np.load('/home/calum/Documents/NumRep/ode/results_rk.npy')
        if method == 'discrete':
            print('Using discrete values for E(x)')
        
    def first_derivative(self,pair):
        if self.method == 'analytic':
            if pair[1] < 1.:
                return 0.
            elif pair[1] < 2.:
                return pair[1]-1
            elif pair[1] < 3.:
                return 3-pair[1]
            else:
                return 0
        # this discrete method requires array with steps half of the required analytic steps due to RK
        elif self.method == 'discrete':
            return self.E[find_t(self.E,pair[1])][0]
    
    def initial_val(self):
        return self.initial
    
    def exact_solution(self,t):
        return None      

# polynomial ODE with arbitrary coefficients y = c[0]+c[1]*x+c{2}*x^2+..
class ode_polynomial:
    def __init__(self,_coeffs):
        print('Creating ODE: polynomial')
        self.coeffs = _coeffs
        self.initial = [self.exact_solution(0.),0.]
        
    def first_derivative(self,pair):
        val = 0.
        for power in range(len(self.coeffs)-1):
            val+=(power+1)*self.coeffs[power+1]*math.pow(pair[1],float(power))
        return val
        # return np.sum([(power+1)*self.coeffs[power+1]*math.pow(pair[1],float(power)) for power in range(len(self.coeffs)-1)])
        
    def initial_val(self):
        return self.initial
    
    def exact_solution(self,t):
        val = 0.
        for power in range(len(self.coeffs)):
            val+=self.coeffs[power]*math.pow(t,float(power))
        return val
        # return np.sum([self.coeffs[power]*math.pow(t,float(power)) for power in range(len(self.

# integration algorithms
class step_euler:
    def dy(self,ode,pair,dt):
        dy = ode.first_derivative(pair)*dt
        return [dy,dt]
    
class step_rk0:
    def dy(self,ode,pair,dt):
        midpoint = [pair[0]+ode.first_derivative(pair)*dt/2.,pair[1]+dt/2.]
        return [ode.first_derivative(midpoint)*dt,dt]
    
class step_rk:
    def dy(self,ode,pair,dt):
        y = pair[0]
        t = pair[1]
        d1 = ode.first_derivative([y,t])
        d2 = ode.first_derivative([y+dt/2.*d1,t+dt/2.])
        d3 = ode.first_derivative([y+dt/2.*d2,t+dt/2.])
        d4 = ode.first_derivative([y+dt*d3,t+dt])
        return [dt*(1./6.)*(d1+2*d2+2*d3+d4),dt]

# engine to run everything
class engine:
    def __init__(self,ode,step,title):
        self.ode = ode
        self.step = step
        self.title = title
        
    def go(self,nsteps,dt):        
        # 2d array [[y0,t0],[y1,t1],...]
        results = []
        # add initial values to results array
        results.append(self.ode.initial_val())
            
        # iterate algorithms
        for i in range(nsteps):
            change = self.step.dy(self.ode,results[i],dt)
            results.append([results[i][0]+change[0],results[i][1]+change[1]])
                    
        print('Engine has finished with',self.title)
        return results  

def main(function,nsteps,delta,voltage_method='discrete'):
    
    print('Running ODE integration for',function,'with nsteps=',nsteps,' and dt=',delta)
    
    # create ODE
    if(function=='electric_field'):
        ode = ode_electric_field(1.)
    elif(function=='voltage'):
        ode = ode_voltage(method=voltage_method)
    else:
        print('Incorrect function input', function)
        quit()
        
    # create integration objects    
    euler_step = step_euler()
    euler_engine = engine(ode,euler_step,'Euler')
    
    rk0_step = step_rk0()
    rk0_engine = engine(ode,rk0_step,'RK0')
    
    rk_step = step_rk()
    rk_engine = engine(ode,rk_step,'RK')
    
    results_euler = euler_engine.go(nsteps,delta)
    results_rk0 = rk0_engine.go(nsteps,delta)
    results_rk = rk_engine.go(nsteps,delta)
    results_exact = [ode.exact_solution(row[1]) for row in results_euler]
    
    plt.figure(figsize=(20,10))
    plt.plot([row[1] for row in results_euler],[row[0] for row in results_euler],'g+',label='Euler')
    plt.plot([row[1] for row in results_rk0],[row[0] for row in results_rk0],'b+',label='RK0')
    plt.plot([row[1] for row in results_rk],[row[0] for row in results_rk],'r+',label='RK4')
    plt.plot([row[1] for row in results_euler],results_exact)
    plt.legend()
    plt.show()
    
    return np.array(results_euler), np.array(results_rk0), np.array(results_rk), np.array(results_exact)
