'''
Script for modelling the forces on neutral Rb-87 atoms in a magneto optical trap
with a single laser and reflection gratings
'''
import os
import sys
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

# User-made modules and functions
sys.path.append( os.path.dirname( os.path.dirname( os.path.abspath(__file__) ) ) )
from src.objects.folders import folders
from src.utilities.makeGrating import *
from src.utilities.physics import *

####################################
# Calculate the magnetic field and lazer intensity in region of atom trap
# and use these to calculate the acceleration experienced by atoms
# within the trapping region and their trajectories.
####################################


''''''''''''''''''''''''''''''''''''
'''         USER OPTIONS         '''
''''''''''''''''''''''''''''''''''''
gratingType = "triangle"    #Choose triangle or square. Default is triangle.
beamRadius = 1.2            #cm 
gaussian = False             #If you want a Gaussian input beam, select True. If not, type False.
radPressure = True         #True: Plot Radiation Pressure, False: Plot Acceleration Profile.
imperfection = False        #Add a faint 0th order diffraction beam.
resolution = 300            #Resolution of image produced, x by x.
xAxis = 0                   #Plot what on x-axis of image? 0 for x, 1 for y, 2 for z.
yAxis = 2                   #Plot what on y-axis of image? 0 for x, 1 for y, 2 for z.
                            #EG: xAxis = 0, yAxis = 2 plots the x-z plane.
rangeX = [-1.55, 1.55]      #Range of x-values (also range seen on plot).
rangeY = [0.0, 0.0]         #Range of y-values (also range seen on plot).
rangeZ = [0.0, 3.1]         #Range of z-values (also range seen on plot).
scaling = 5.                #Scale factor for the acceleration vectors.



# Get grating geometry and properties
if gratingType == "square":
    gratings = makeSquareGrating()
elif gratingType == "triangle":
    gratings = makeTriangleGrating()
else:
    gratings = makeSquareGrating()


# Acceleration magnitude and x & y component arrays.
a = np.zeros((resolution, resolution), dtype=float)
aV = np.zeros((resolution, resolution), dtype=float)
aH = np.zeros((resolution, resolution), dtype=float)

# Use the user options to create iCheck and jCheck.
# These lists ensure that the correct axes are used.
iCheck = [0., 0., 0.]
jCheck = [0., 0., 0.]
iCheck[yAxis] = 1.
jCheck[xAxis] = 1.

labels = ['x', 'y', 'z']
if radPressure == True:
    print("Generating Radiation Pressure Profile in %s-%s Plane" % (labels[xAxis], labels[yAxis]))
else:
    print("Generating Acceleration Profile in %s-%s Plane" % (labels[xAxis], labels[yAxis]))

# Calculate the force field
for i in range(len(a)):
    sys.stdout.write('\rProgress: {0:.2f}%'.format(i*100/resolution+1))
    sys.stdout.flush()
    for j in range(len(a[0])):
        # Generate coordinate [x, y, z].
        x = rangeX[0] + (rangeX[1]-rangeX[0])*(i*iCheck[0] + j*jCheck[0])/float(resolution-1)
        y = rangeY[0] + (rangeY[1]-rangeY[0])*(i*iCheck[1] + j*jCheck[1])/float(resolution-1)
        z = rangeZ[0] + (rangeZ[1]-rangeZ[0])*(i*iCheck[2] + j*jCheck[2])/float(resolution-1)
        
        # Compute acceleration or radiation pressure from incident laser beam.
        intensity = 1
        if gaussian == True:
            intensity *= np.e**(-(x**2 + y**2)/2.)
        K = np.array([0., 0., -1.])
        if x**2 + y**2 <= beamRadius**2:
            if radPressure == True:
                F = intensity*K
            else:
                F = acceleration(K, [x, y, z], I=intensity)
        else:
            F = np.array([0., 0., 0.])
        
        # Compute acceleration or radiation pressure from 0th order beam.
        if imperfection == True:
            intensity = 0.01
            if gaussian == True:
                intensity *= np.exp(-(0.5*x)**2)
            K = np.array([0., 0., 1.])
            if x**2 + y**2 <= beamRadius**2:
                if radPressure == True:
                    F = intensity*K
                else:
                    F += acceleration(K, [x, y, z], I=intensity, factor=-1.)
        
        temp = True
        for grating in gratings:
            if temp == True:
                temp = False
                factor = -1
            else:
                factor = 1
            
            # Compute acceleration or radiation pressure from kth grating 1st order beam.
            intensity = grating.reflectivity * grating.intensity(
                [x, y, z], 
                factor, 
                beamRadius, 
                gaussian=gaussian
            )
            
            
            # Unit vector of diffracted beam
            kUnit = grating.k/np.sqrt(np.dot(grating.k, grating.k))
            
            if intensity[0] != 0.:
                if radPressure == True:
                    F += kUnit * intensity[0]
                else:
                    F += acceleration(kUnit, [x, y, z], I=intensity[0], factor=-1.)
            
            # Compute acceleration or radiation pressure from kth grating 1st order beam in other direction.
            intensity = grating.reflectivity * grating.intensity(
                [x, y, z], 
                -factor, 
                beamRadius, 
                gaussian=gaussian
            )
            
            if intensity[0] != 0.:
                if radPressure == True:
                    F += kUnit * intensity[0]
                else:
                    F += acceleration(kUnit, [x, y, z], I=intensity[0], factor=-1.)
        
        # Store the acceleration magnitude and the components of the acceleration.
        a[i][j] = np.sqrt(np.dot(F, F))
        aH[i][j] = F[xAxis]
        aV[i][j] = F[yAxis]
        

# Generate grid of acceleration vectors.        
ranges = [rangeX, rangeY, rangeZ]                
x = np.linspace(ranges[xAxis][0], ranges[xAxis][1], resolution)
z = np.linspace(ranges[yAxis][0], ranges[yAxis][1], resolution)
div = 15            # Determines NxN grid of vectors.
X = np.linspace(ranges[xAxis][0], ranges[xAxis][1], div)
Z = np.linspace(ranges[yAxis][0], ranges[yAxis][1], div)
u = np.zeros((div, div))
v = np.zeros((div, div))
fake = np.zeros((div, div))
for i in range(div):
    for j in range(div):
        u[i][j] = aH[round(i*(resolution-1)/(div-1))][round(j*(resolution-1)/(div-1))]
        v[i][j] = aV[round(i*(resolution-1)/(div-1))][round(j*(resolution-1)/(div-1))]
if np.max(a) != 0.:
    u = u/abs(scaling*np.max(a))
    v = v/abs(scaling*np.max(a))
a *= 1/float(np.max(a))
(X, Z) = np.meshgrid(X, Z)


###############################################
#######            Plotting             #######
###############################################
name = gratingType.title() + " grating"
filename = os.path.join(sys.path[0], "acceleration_field.png")

plt.figure()

if radPressure == True:
    my_cmap = plt.cm.get_cmap('hot')
else:
    my_cmap = plt.cm.get_cmap('jet_r')

CS = plt.pcolor(x, z, a, 
                  cmap=my_cmap)
cbar = plt.colorbar(CS)

plt.quiver(X, Z, u, v, angles='xy', scale=1, color='#555555')
if radPressure == True:
    cbar.ax.set_ylabel('Relative Radiation Pressure')
else:
    cbar.ax.set_ylabel('Acceleration (Relative)')
plt.axis([ranges[xAxis][0], ranges[xAxis][1], ranges[yAxis][0], ranges[yAxis][1]])
plt.xlabel('$%s$ ($cm$)' % (labels[xAxis]))
plt.ylabel('$%s$ ($cm$)' % (labels[yAxis]))
if radPressure == True:
    plt.title('%s, Radiation Pressure in %s-%s Plane' % (name, labels[xAxis], labels[yAxis]))
else:
    plt.suptitle('%s, Acceleration of $^{87}$Rb Atoms in %s-%s Plane' % (name, labels[xAxis], labels[yAxis]))
    if gaussian == True:
        plt.title('Gaussian Beam, $I_0 = 100\\ Wm^{-2}$, $\\frac{dB}{dr} = 0.15 \ T\ m^{-1}$, $z_0=0.55cm$')
    else:
        plt.title('Uniform Beam, $I_0 = 100\\ Wm^{-2}$, $\\frac{dB}{dr} = 0.15 \ T\ m^{-1}$, $z_0=0.55cm$')
plt.savefig(filename, dpi=200)
plt.close()
