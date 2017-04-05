from Chisq     import *
from numpy import matrix
import scipy.optimize as theMinimiser


print("Reading in data")
data = np.loadtxt("testData.txt")
print(str(data))

# Create column vectors from the data
xdata = np.matrix(data[:, 0]).T
ydata = np.matrix(data[:, 1]).T
edata = np.matrix(data[:, 2]).T
    
print("Create a ChiSq object")
theChisq = ChiSq( xdata, ydata, edata, Linear())

print("Minimise the chisq")
result = theMinimiser.minimize( theChisq.evaluateForOptimize, [0.0,1.5])

#print ("Minimisation finished")
print result
