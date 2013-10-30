#!/usr/bin/env python
"""
Author: Timothy A.V. Teatro <http://www.timteatro.net>
Date  : Oct 25, 2010
Lisence: Creative Commons BY-SA
(http://creativecommons.org/licenses/by-sa/2.0/)

Description:
	A program which uses an explicit finite difference
	scheme to solve the diffusion equation with fixed
	boundary values and a given initial value for the
	density u(x,y,t). This version uses a numpy
	expression which is evaluated in C, so the
	computation time is greatly reduced over plain
	Python code.

	This version also uses matplotlib to create an
	animation of the time evolution of the density.
"""
import scipy as sp
import matplotlib
matplotlib.use('GTKAgg') # Change this as desired.
import gobject
from pylab import *
# Declare some variables:

dx=0.01        # Interval size in x-direction.
dy=0.01        # Interval size in y-direction.
a=0.5          # Diffusion constant.
timesteps=500  # Number of time-steps to evolve system.

nx = int(1/dx)
ny = int(1/dy)

dx2=dx**2 # To save CPU cycles, we'll compute Delta x^2
dy2=dy**2 # and Delta y^2 only once and store them.

# For stability, this is the largest interval possible
# for the size of the time-step:
dt = dx2*dy2/( 2*a*(dx2+dy2) )

# Start u and ui off as zero matrices:
ui = sp.zeros([nx,ny])
u = sp.zeros([nx,ny])

# Now, set the initial conditions (ui).
for i in range(nx):
	for j in range(ny):
		if ( ( (i*dx-0.5)**2+(j*dy-0.5)**2 <= 0.1)
			& ((i*dx-0.5)**2+(j*dy-0.5)**2>=.05) ):
				ui[i,j] = 1

def evolve_ts(u, ui):
	"""
	This function uses a numpy expression to
	evaluate the derivatives in the Laplacian, and
	calculates u[i,j] based on ui[i,j].
	"""
	u[1:-1, 1:-1] = ui[1:-1, 1:-1] + a*dt*( (ui[2:, 1:-1] - 2*ui[1:-1, 1:-1] + ui[:-2, 1:-1])/dx2 + (ui[1:-1, 2:] - 2*ui[1:-1, 1:-1] + ui[1:-1, :-2])/dy2 )

def updatefig(*args):
	global u, ui, m
	im.set_array(ui)
	manager.canvas.draw()
	# Uncomment the next two lines to save images as png
	# filename='diffusion_ts'+str(m)+'.png'
	# fig.savefig(filename)
	u[1:-1, 1:-1] = ui[1:-1, 1:-1] + a*dt*(
		(ui[2:, 1:-1] - 2*ui[1:-1, 1:-1] + ui[:-2, 1:-1])/dx2
		+ (ui[1:-1, 2:] - 2*ui[1:-1, 1:-1] + ui[1:-1, :-2])/dy2 )
	ui = sp.copy(u)
	m+=1
	print "Computing and rendering u for m =", m
	if m >= timesteps:
		return False
	return True

fig = plt.figure(1)
img = subplot(111)
im = img.imshow( ui, cmap=cm.hot, interpolation='nearest', origin='lower')
manager = get_current_fig_manager()

m=1
fig.colorbar( im ) # Show the colorbar along the side

# once idle, call updatefig until it returns false.
gobject.idle_add(updatefig)
show()

