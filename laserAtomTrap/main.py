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
from src.grating import grating
from src.physics import *

####################################
#Calculate the magnetic field and lazer intensity in region of atom trap
#and use these to calculate the acceleration experienced by atoms
#within the trapping region and their trajectories.
####################################


''''''''''''''''''''''''''''''''''''
'''         USER OPTIONS         '''
''''''''''''''''''''''''''''''''''''
grating_type = "triangle"   #Choose triangle or square. Default is triangle.
beam_radius = 1.2           #cm 
gaussian = True             #If you want a Gaussian input beam, select True. If not, type False.
rad_press = False           #True: Plot Radiation Pressure, False: Plot Acceleration Profile.
imperfection = False        #Add a faint 0th order diffraction beam.
resolution = 300            #Resolution of image produced, x by x.
x_axis = 0                  #Plot what on x-axis of image? 0 for x, 1 for y, 2 for z.
y_axis = 2                  #Plot what on y-axis of image? 0 for x, 1 for y, 2 for z.
                            #EG: x_axis = 0, y_axis = 2 plots the x-z plane.
x_range = [-1.55,1.55]      #Range of x-values (also range seen on plot).
y_range = [0.0,0.0]         #Range of y-values (also range seen on plot).
z_range = [0.0,3.1]         #Range of z-values (also range seen on plot).
scaling = 5.                #Scale factor for the acceleration vectors.



    

gratings = []
''''''''''''''''''''''''''''''''''''
'''        Square Grating.       '''
''''''''''''''''''''''''''''''''''''
if grating_type == "square":
    name = "Square Grating"
    angle = np.pi/2.0 - 41 * np.pi / 180.0
    angle2 = 41 * np.pi / 180.0
    reflectivity = 1/(4.*np.cos(angle2))
    
    ''' x > -1, x < 1, y > -1, y < 1 '''
    space = [[1,0,1.],[-1,0,1.],[0,1,1.],[0,-1,1.]]
    
    gratings.append( grating(space, np.array([1,0]), angle, reflectivity) )
    gratings.append( grating(space, np.array([0,1]), angle, reflectivity) )


''''''''''''''''''''''''''''''''''''
'''        Triangular Grating.   '''
''''''''''''''''''''''''''''''''''''
if grating_type == "triangle" or grating_type != "square":
    name = "Triangular Grating"
    angle = np.pi/2.0 - 41 * np.pi / 180.0
    angle2 = 41* np.pi / 180.0
    reflectivity = 1/(3.*np.cos(angle2))
    tan_60 = np.tan(60 * np.pi / 180.0)
    sin_60 = np.sin(60 * np.pi / 180.0)
    cos_60 = np.cos(60 * np.pi / 180.0)
    tan_30 = np.tan(30 * np.pi / 180.0)
    sin_30 = np.sin(30 * np.pi / 180.0)
    cos_30 = np.cos(30 * np.pi / 180.0)
    
    '''Grating 1 dimensions.'''
    ''' x > -1.2, tan(60)*x + y < 0, -tan(60)*x + y > 0 '''
    space1 = [[1,0,1.2],[-tan_60,-1,0.],[-tan_60,1,0.]]
    '''Grating 3 dimensions.'''
    ''' tan(60)*x + y > 0, x < 1.2, y > 0, y < 1.2 '''
    space2 = [[tan_60,1,0.],[-1,0,1.2],[0,1,0.],[0,-1,1.2]]
    '''Grating 2 dimensions.'''
    ''' tan(60)*x - y > 0, x < 1.2, y < 0, y > -1.2 '''
    space3 = [[tan_60,-1,0.],[-1,0,1.2],[0,-1,0.],[0,1,1.2]]
    
    gratings.append( grating(space1, np.array([0,1]), angle, reflectivity) )
    gratings.append( grating(space2, np.array([-cos_30,sin_30]), angle, reflectivity) )
    gratings.append( grating(space3, np.array([cos_30,sin_30]), angle, reflectivity) )

#Acceleration magnitude and x & y component arrays.
acc = np.zeros((resolution,resolution),dtype=float)
acc_vert = np.zeros((resolution,resolution),dtype=float)
acc_hor = np.zeros((resolution,resolution),dtype=float)

#Use the user options to create i_check and j_check.
#These lists ensure that the correct axes are used.
i_check = [0.,0.,0.]
j_check = [0.,0.,0.]
i_check[y_axis] = 1.
j_check[x_axis] = 1.

labels = ['x','y','z']
if rad_press == True:
    print "Generating Radiation Pressure Profile in %s-%s Plane" % (labels[x_axis],labels[y_axis])
else:
    print "Generating Acceleration Profile in %s-%s Plane" % (labels[x_axis],labels[y_axis])
for i in range(len(acc)):
    sys.stdout.write('\rProgress: {0}%'.format(i*100/resolution+1))
    sys.stdout.flush()
    for j in range(len(acc[0])):
        #Generate coordinate [x,y,z].
        x = x_range[0] + (x_range[1]-x_range[0])*(i*i_check[0] + j*j_check[0])/float(resolution-1)
        y = y_range[0] + (y_range[1]-y_range[0])*(i*i_check[1] + j*j_check[1])/float(resolution-1)
        z = z_range[0] + (z_range[1]-z_range[0])*(i*i_check[2] + j*j_check[2])/float(resolution-1)
        
        #Compute acceleration or radiation pressure from incident laser beam.
        intensity = 1
        if gaussian == True:
            intensity *= np.e**(-(x**2 + y**2)/2.)
        K = np.array([0.,0.,-1.])
        if x**2 + y**2 <= beam_radius**2:
            if rad_press == True:
                F = intensity*K
            else:
                F = a(K,[x,y,z],angle2,I=intensity)
        else:
            F = np.array([0.,0.,0.])
        
        #Compute acceleration or radiation pressure from 0th order beam.
        if imperfection == True:
            intensity = 0.01
            if gaussian == True:
                intensity *= np.exp(-(0.5*x)**2)
            K = np.array([0.,0.,1.])
            if x**2 + y**2 <= beam_radius**2:
                if rad_press == True:
                    F = intensity*K
                else:
                    F += a(K,[x,y,z],angle2,I=intensity,factor=-1.)
        
        temp = True
        for k in gratings:
            if temp == True:
                temp = False
                factor = -1
            else:
                factor = 1
            
            #Compute acceleration or radiation pressure from kth grating 1st order beam.
            temp1 = k.intensity([x,y,z],factor,beam_radius,gaussian=gaussian)
            intensity = temp1[0]
            K = k.kvector
            unit_K = K/np.sqrt(np.dot(K,K))
            if intensity != 0.:
                if rad_press == True:
                    F += unit_K * reflectivity * intensity
                else:
                    F += a(unit_K,[x,y,z],angle2,I=reflectivity*intensity,factor=-1.)
            
            #Compute acceleration or radiation pressure from kth grating 1st order beam in other direction.
            temp2 = k.intensity([x,y,z],-factor,beam_radius,gaussian=gaussian)
            intensity = temp2[0]
            K = k.kvector
            unit_K = K/np.sqrt(np.dot(K,K))
            if intensity != 0.:
                if rad_press == True:
                    F += unit_K * reflectivity * intensity
                else:
                    F += a(unit_K,[x,y,z],angle2,I=reflectivity*intensity,factor=-1.)
        
        #Store the acceleration magnitude and the components of the acceleration.
        acc[i][j] = np.sqrt(np.dot(F,F))
        acc_hor[i][j] = F[x_axis]
        acc_vert[i][j] = F[y_axis]
        

#Generate grid of acceleration vectors.        
ranges = [x_range,y_range,z_range]                
x = np.linspace(ranges[x_axis][0],ranges[x_axis][1],resolution)
z = np.linspace(ranges[y_axis][0],ranges[y_axis][1],resolution)
div = 15            #Determines NxN grid of vectors.
X = np.linspace(ranges[x_axis][0],ranges[x_axis][1],div)
Z = np.linspace(ranges[y_axis][0],ranges[y_axis][1],div)
u = np.zeros((div,div))
v = np.zeros((div,div))
fake = np.zeros((div,div))
for i in range(div):
    for j in range(div):
        u[i][j] = acc_hor[i*(resolution-1)/(div-1)][j*(resolution-1)/(div-1)]
        v[i][j] = acc_vert[i*(resolution-1)/(div-1)][j*(resolution-1)/(div-1)]
if np.max(acc) != 0.:
    u = u/abs(scaling*np.max(acc))
    v = v/abs(scaling*np.max(acc))
acc *= 1/float(np.max(acc))
(X,Z) = np.meshgrid(X,Z)


###############################################
#######            Plotting             #######
###############################################
plt.figure()

if rad_press == True:
    my_cmap = plt.cm.get_cmap('hot')
else:
    my_cmap = plt.cm.get_cmap('jet_r')

CS = plt.pcolor(x, z, acc,
                  cmap=my_cmap)
cbar = plt.colorbar(CS)

plt.quiver(X,Z,u,v,angles='xy',scale=1,color='#555555')
if rad_press == True:
    cbar.ax.set_ylabel('Relative Radiation Pressure')
else:
    cbar.ax.set_ylabel('Acceleration (Relative)')
plt.axis([ranges[x_axis][0],ranges[x_axis][1],ranges[y_axis][0],ranges[y_axis][1]])
plt.xlabel('$%s$ ($cm$)' % (labels[x_axis]))
plt.ylabel('$%s$ ($cm$)' % (labels[y_axis]))
if rad_press == True:
    plt.title('%s, Radiation Pressure in %s-%s Plane' % (name,labels[x_axis],labels[y_axis]))
else:
    plt.suptitle('%s, Acceleration of $^{87}$Rb Atoms in %s-%s Plane' % (name,labels[x_axis],labels[y_axis]))
    if gaussian == True:
        plt.title('Gaussian Beam, $I_0 = 100\\ Wm^{-2}$, $\\frac{dB}{dr} = 0.15 \ T\ m^{-1}$, $z_0=0.55cm$')
    else:
        plt.title('Uniform Beam, $I_0 = 100\\ Wm^{-2}$, $\\frac{dB}{dr} = 0.15 \ T\ m^{-1}$, $z_0=0.55cm$')
plt.savefig(os.path.join(sys.path[0], "acceleration_field.png"))
plt.close()
