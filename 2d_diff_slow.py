#!/usr/bin/env python
"""
A program which uses an explicit finite difference
scheme to solve the diffusion equation with fixed
boundary values and a given initial value for the
density.

Two steps of the solution are stored: the current
solution, u, and the previous step, ui. At each time-
step, u is calculated from ui. u is moved to ui at the
end of each time-step to move forward in time.

"""
import scipy as sp
import time

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
	global nx, ny
	"""
	This function uses two plain Python loops to
	evaluate the derivatives in the Laplacian, and
	calculates u[i,j] based on ui[i,j].
	"""
	for i in range(1,nx-1):
		for j in range(1,ny-1):
			uxx = ( ui[i+1,j] - 2*ui[i,j] + ui[i-1, j] )/dx2
			uyy = ( ui[i,j+1] - 2*ui[i,j] + ui[i, j-1] )/dy2
			u[i,j] = ui[i,j]+dt*a*(uxx+uyy)

# Now, start the time evolution calculation...
tstart = time.time()
for m in range(1, timesteps+1):
	evolve_ts(u, ui)
	print "Computing u for m =", m
	ui = u.copy()
tfinish = time.time()

print "Done."
print "Total time: ", tfinish-tstart, "s"
print "Average time per time-step using numpy: ", ( tfinish - tstart )/timesteps, "s."

