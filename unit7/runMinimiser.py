from Chisq     import *
from Minimiser import *
from numpy import matrix

print("Create a minimiser object")
theMinimiser = Minimiser()

print("Set the initial parameters")
params     = matrix([0., 1.5]).T
increments = matrix([0.01, 0.01]).T
theMinimiser.set_StartParams(params, increments)
    

print("Reading in data")
data = np.loadtxt("testData.txt")
print(str(data))

    
# Create column vectors from the data
xdata = np.matrix(data[:, 0]).T
ydata = np.matrix(data[:, 1]).T
edata = np.matrix(data[:, 2]).T
    
print("Create a ChiSq object")
theChisq = ChiSq( xdata, ydata, edata, Linear())


#Set the staring parameters
startParams = [0.,1.5]
increments = [0.01, 0.01]
theChisq.setParameters(params)
theMinimiser.set_StartParams(startParams, increments)


print("Starting the minimisation loop")
while(theMinimiser.get_isFinished() != True):
    params = theMinimiser.minimise(theChisq.evaluate())
    theChisq.setParameters(params)
        
print ("Minimisation finished")
print ("   Final chisq = "+str(theChisq.evaluate()))
print ("   Final parameters:  m = "+str(params[0])+"  / c = "+str(params[1]))
