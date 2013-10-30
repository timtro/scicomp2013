# create array
import numpy as np
a = np.arange(10)
a.dtype
a.itemsize

# slicing
a[1:4]
a[1:-2]
a[-6:8]
a[0:9:2]
a[:4]
a[7:]
a[-2:]
a[::2]

# masking
idx = [1,5,7,8]
a[idx]
mask = ( a <= 5 )
a[mask]

#plotting
import pylab as pl
x = np.linspace(0, 2*np.pi, 25)
y = np.sin(x)
mask = np.logical_and(y >= -.5, y <= .5)
pl.plot(x, y, 'b-')
pl.plot(x[mask], y[mask], 'ro')
pl.show()

# differentiate sin(x)
dydx = (y[1:] - y[:-1]) / (x[1:] - x[:-1])
pl.plot(x, y, 'b-')
pl.plot(x[1:], dydx, 'r-')
pl.show()

# integrate sin(x)
intydx = np.cumsum(y)[1:] * (x[1:]-x[:-1])
pl.plot(x, y)
pl.plot(x[1:], intydx - 1)
pl.show()

# 2D arrays
m = np.arange(9).reshape(3,3)
list = [[4, 3, 2], [5,4,3], [6,5,4]]
n = np.array(list)
m.shape
m.size
m.ndim
m+n
m*n

# Exportind data as csv
np.savetxt('m.csv', m, delimiter=',')
new_m = np.genfromtxt('m.csv', delimiter=',')

