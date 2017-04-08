import numpy as np
import math

class MyGaussianPdf:


    #............................
    #Constructors
    def __init__(self, mean, width):
        self.mean = float(mean)   #number of rows
        self.width = float(width)   #number of columns
 
 
    #............................
    #Method to return value of Gaussian at point x
    def evaluate(self, x):
        val = math.exp( -(x-self.mean)**2 / (2.0 * self.width**2 ))
        return val

    # @vectorize([float32(float32)])
    # def evaluatevec(self, x):
    #     val = math.exp( -(x-self.mean)**2 / 2.0 / self.width**2 )
    #     return val

    #............................
    #Method to return maximum value of Gaussian at point x
    def max(self ):
        return 1.0
    

    #............................
    #Method to return a random number with a Gaussian distribution in +- 3 sigma
    def next( self ):
        
        test1 = 0.
        test2 = 0.
        test3 = 1.
        while ( test3 > test2 ):
            test1 = (np.random.uniform() -0.5) * 2.0
            test1 = test1 * self.width * 3.0 + self.mean
            test2 = self.evaluate( test1)
            test3 = np.random.uniform() * self.max()
        
        return test1
    
    
    #............................
    #Method to do numerical integration
    #This is written in a very simplistic way.
    

    def integralNumeric( self, ilo, ihi ):

        npoints = 1000000
        ninside = 0
        lo = float(ilo)
        hi = float(ihi)

        for i in range(npoints):
            x = lo + np.random.uniform()*(hi-lo)
            y = np.random.uniform()*self.max()
            if( y < self.evaluate(x)): ninside = ninside+1

        Atot = (hi-lo)*self.max()
        eff = float(ninside)/float(npoints)
        
        #Area
        Area = Atot * eff
        #Binomial error
        Error = Atot*math.sqrt(eff*(1-eff)/npoints)

        return Area, Error
            
    #............................
    #Method to do numerical integration
    #This is written using numpy arrays and numpy array functions
    #The operations are done in parallel on the whole array (vectorised)
    def integralNumericFaster( self, ilo, ihi ):
        
        npoints = 1000000
        lo = float(ilo)
        hi = float(ihi)

        # evaluate the argument to the exponential in the function (see the above method evaluate())
        # -> val = math.exp( -(x-self.mean)**2 / (2.0 / self.width**2 )
        # the numpy math methods are really fast when used on arrays.  It's important
        # NOTE: if you are working on a *scalar*, the standard math library is faster.
        xlist = np.square((np.random.uniform(lo,hi, npoints)-self.mean))/(2.0*self.width**2)
        # now exponentiate all of the x entries
        yeval = np.exp(-xlist)
        ylist = np.random.uniform(0., self.max(), npoints)
        comp = np.less( ylist, yeval )
        ninside = np.sum(comp)

        Atot = (hi-lo)*self.max()
        eff = float(ninside)/float(npoints)
        
        #Area
        Area = Atot * eff
        #Binomial error
        Error = Atot*math.sqrt(eff*(1-eff)/npoints)
        
        return Area, Error



    #............................
    #Method to do analytic integration
    # This is lazt version wiuch assumed limits are very large
    # So lo and hi are ignored

    def integralAnalytic( self, lo, hi ):

        integral = self.width*math.sqrt(2.0*math.pi )
        return integral


