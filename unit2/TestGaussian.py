from MyGaussianPdf import *
import time


# .....................................................................
# Generate  random numbers using my own generator

print("This is my own random number generator  .. printing first 10 numbers")

mygauss = MyGaussianPdf( 0.0, 1.0 )

npoints = 1000

data =[]

for i in range(npoints):
    data.append( mygauss.next() )

for i in range(10):
    print(str(data[i]))
print(" .....for "+str(npoints)+" numbers")


np.savetxt( "myGaussianOutput.txt", data)




# .....................................................................
# Generate  random numbers using numpy generator.

print("This is the numpy gaussian number generator  .. printing first 10 numbers")

npoints = 1000

data = np.random.normal( 0.0, 1.0, npoints )

for i in range(10):
    print(str(data[i]))
print(" .....for "+str(npoints)+" numbers")


np.savetxt( "numpyGaussianOutput.txt", data)




# .....................................................................
# Test numerical integration.

integralAnalytic = mygauss.integralAnalytic(-5.0, 5.0 )

print("Slow integral:")
start= time.time()
integralNumeric1 = mygauss.integralNumeric(-5.0, 5.0 )
end= time.time()
print("...took "+str(end-start)+"  secs")

print("Faster integral:")
start= time.time()
integralNumeric2 = mygauss.integralNumericFaster(-5.0, 5.0 )
end= time.time()
print("...took "+str(end-start)+"  secs")


print(" Integrals: ")
print("  analytic  "+str(integralAnalytic))
print("  numeric1  "+str(integralNumeric1))
print("  numeric2  "+str(integralNumeric2))