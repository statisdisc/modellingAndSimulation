'''
Code which randomly produces an electrical circuit with series of straight wires.
If a minimum in the magnetic field (a well) is found at the centre of the domain
then the set-up is useful for trapping neutral atoms and is output by the code.

To do: Put sections of code below into functions to make main.py cleaner and clearer
'''
import numpy as np
import random as rn
import sys
import os
import time
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.lines as mlines
from matplotlib import gridspec
from scipy.optimize import curve_fit

# User-made modules and functions
from src.wire import wire

''''''''''''''''''''''''''''''''''''
'''         USER OPTIONS         '''
''''''''''''''''''''''''''''''''''''
resolution = 299                    #x by x data points in final contour plot.
rot = 0.5                           #1.0 = Rotational Symmetry, 0.0 = Reflectional Symmetry.
                                    #Anything in-between: Corresponding probability of each.
bias = True                         #True = Magnetic Bias Field Applied, False = Not Applied.
N_min = 4                           #Minimum number of randomly generated wires.
N_max = 5                           #Maximum number of randomly generated wires.
Nconfigs = 5                        #Number of configurations to be output by the code.
directory = sys.path[0]             #Directory of image files to be saved. Default: Directory of code.




#Produce Nconfigs wires.
for Nconfig in range(Nconfigs):
    #Give resolution and size of arrays.
    size = resolution
    field = np.zeros((size,size))                #B-field array.

    #x, y and z axis coordinate arrays.
    X = np.linspace(-size/2.0,size/2.0,size)    
    Y = np.linspace(-size/2.0,size/2.0,size)
    Z = np.linspace(3,50,200)

    #B-field component and magnitude arrays along x-axis.
    x_B_x = np.zeros(size)
    x_B_y = np.zeros(size)
    x_B_z = np.zeros(size)
    x_B = np.zeros(size)
    #B-field component and magnitude arrays along y-axis.
    y_B_x = np.zeros(size)
    y_B_y = np.zeros(size)
    y_B_z = np.zeros(size)
    y_B = np.zeros(size)
    #B-field component and magnitude arrays along z-axis.
    z_B = np.zeros(len(Z))

    #Additional arrays for extra analysis.
    XY = np.linspace(0,size,49)
    y_B2 = np.zeros(len(XY))
    x_B2 = np.zeros(len(XY))
    x_B3 = np.zeros(len(XY))

    #Set the default magnetic bias field and the trial range.
    if bias == True:
        B_bias =  19.9
        Bbias = np.linspace(3,30,30)
    else:
        B_bias = 0
        Bbias = np.zeros(30)

    z=10.0

    '''
    #Wire Vertices
    #Template vertices for the popular Z-trap.
    vertices = [
                [-1.,0.9],
                [0.5,0.9],
                [0.5,0.1],
                [2.0,0.1]
                        ]

    #Create list of wires involved.
    wires = []
    for i in range(len(vertices)-1):
        vertices[i+1][0] += (2*rn.random()-1)/10.0
        wires.append(wire(vertices[i],vertices[i+1],size=size))
    '''

    #Initial wire vertices
    random_vertex = 0.5 + rn.random()/2.0
    vertices = [
                [-3.,0.9],
                [0.0,random_vertex]
                        ]
    #Initial wire array.
    wires = [wire(vertices[0],vertices[1],size=size)]

    #Choose number of randomly generated wires.
    N = rn.randint(N_min,N_max)
    #Keep track of number of attempts to generate each wire.
    attempts = np.zeros((N),dtype=int)

    #If success is True, a valid wire configuration has been found.    
    success = False

    i = -1            #Counter
    while success == False:        
        while i < N-1:
            i += 1
            while len(wires) == 1 + i:
                while True:
                    attempts[i] += 1
                    if attempts[i] == 11:
                        if i != 0:
                            break
                    
                    print i*'\t' + 'Generating Wire {0}, Attempt {1}'.format(i+1,attempts[i])
                    
                    #Set a range for the x-coordinate of the random point.
                    lower_limit = -vertices[i+1][0]
                    upper_limit = 1.0 - vertices[i+1][0]
                    vertex_x = vertices[i+1][0] + rn.uniform(lower_limit,upper_limit)
                    
                    #Set a range for the y-coordinate of the random point.
                    lower_limit = 0.5 - vertices[i+1][1]
                    upper_limit = 1 - vertices[i+1][1]
                    vertex_y = vertices[i+1][1] + rn.uniform(lower_limit,upper_limit)
                    
                    new_vertex = [vertex_x,vertex_y]
                    new_wire = wire(vertices[i+1],new_vertex,size=size)
                    
                    intersect = False
                    
                    for j in range(len(wires)):
                        #Make sure wire doesn't intersect any other wires
                        #and that the angle it makes isn't too extreme.
                        if new_wire.intersect(wires[j]) == True or new_wire.angle(wires[j]) > 7*np.pi/8.0:
                            intersect = True
                            break
                    if intersect == True:
                        break
                    
                    #If no wires intersect, accept the wire and move on to the next one.
                    wires.append(new_wire)
                    vertices.append(new_vertex)
                    break
                
                #If wire generator gets stuck (backed into a corner),
                #go back an iteration and replace that previous wire.
                if attempts[i] == 11:
                    if i != 0:
                        attempts[i] = 0
                        i += -2
                        del wires[-1]
                        del vertices[-1]
                        break
            
            #Add final wire which connects to center of region.
            if i == N-1:
                print N*'\t' + "Attempting to Generate Final Wire"
                new_wire = wire(vertices[-1],[0.5,0.5],size=size)
                
                #Also make sure wire doesn't intersect and angle isn't too extreme.
                intersect = False
                for j in range(len(wires)):
                    condition1 = new_wire.intersect(wires[j]) == True
                    condition2 = new_wire.angle(wires[j]) < np.pi/4.0
                    condition3 = new_wire.angle(wires[j]) > 7*np.pi/8.0
                    if condition1 or condition3:
                        intersect = True
                        break
                
                #If final wire fails
                #go back an iteration and replace previous wire.
                #If success, add final wire.
                if intersect == True:
                    i += -1
                    del wires[-1]
                    del vertices[-1]
                else:
                    wires.append(new_wire)
                    vertices.append([0.5,0.5])
                    
        if rn.random() <= rot:
            #Create Rotational Symmetry.
            for m in range(N+2):
                vertex_x = -vertices[N+1-m][0] + 1.0
                vertex_y = -vertices[N+1-m][1] + 1.0
                vertices.append([vertex_x,vertex_y])
                wires.append(wire(vertices[N+2+m],[vertex_x,vertex_y],size=size))
        else:
            #Create Reflection Symmetry.
            for m in range(N+2):
                vertex_x = vertices[N+1-m][0]
                vertex_y = -vertices[N+1-m][1] + 1.0
                vertices.append([vertex_x,vertex_y])
                wires.append(wire(vertices[N+2+m],[vertex_x,vertex_y],size=size))

        #Calculate the magnetic field along the z-axis.
        print "Generating B_z Profile"
        for n in range(len(Z)):
            B_vector = np.array([B_bias,0.,0.])
            for k in wires:
                B_vector += k.B_vec([size/2,size/2,Z[n]])
            mod_B = np.sqrt(B_vector[0]**2 + B_vector[1]**2 + B_vector[2]**2)
            z_B[n] = mod_B
        if min(z_B) == z_B[0] or min(z_B) == z_B[-1]:
            print "Wire Failed: No Stable Minimum Found."
            i = -1
            attempts = np.zeros((N),dtype=int)
        #Continue if a minimum is found.
        else:
            z = Z[np.argmin(z_B)]
            success = True
        
            #Adjust the bias field to optimise the trap.
            print "Adjusting Bias Field"
            B_vector = np.array([0.,0.,0.])
            for k in wires:
                B_vector += k.B_vec([size/2.,size/2.,z])
            B_bias = -B_vector[0]
            print "Bias Field: {0}mT".format(B_bias)
            
            #Generate the magnetic fields along the x and y axes.
            print "Generating B_x and B_y Profiles"
            for n in range(len(XY)):
                B_vector1 = np.array([B_bias,0.,0.])
                B_vector2 = np.array([B_bias,0.,0.])
                for k in wires:
                    B_vector1 += k.B_vec([XY[n],size/2,z])
                    B_vector2 += k.B_vec([size/2,XY[n],z])
                x_B2[n] = np.sqrt(B_vector1[0]**2 + B_vector1[1]**2 + B_vector1[2]**2)
                y_B2[n] = np.sqrt(B_vector2[0]**2 + B_vector2[1]**2 + B_vector2[2]**2)
                
            #If there is no central minimum on the x and y axes, reject the wire.
            if min(x_B2) != x_B2[len(x_B2)/2] or min(y_B2) != y_B2[len(y_B2)/2]:
                print "Wire Failed: No Stable Minimum Found."
                i = -1
                attempts = np.zeros((N),dtype=int)
                success = False
            
            #Generate another magnetic profile along the z axis, now that the bias field has been adjusted.
            print "Generating Final B_z Profile"
            for n in range(len(Z)):
                B_vector = np.array([B_bias,0.,0.])
                for k in wires:
                    B_vector += k.B_vec([size/2.,size/2.,Z[n]])
                mod_B = np.sqrt(B_vector[0]**2 + B_vector[1]**2 + B_vector[2]**2)
                z_B[n] = mod_B
            if min(z_B) == z_B[0] or min(z_B) == z_B[-1]:
                print "Wire Failed: No Stable Minimum Found."
                i = -1
                attempts = np.zeros((N),dtype=int)
                success = False

        #If the wire has failed, start from scratch.
        if success == False:
            #Initial vertices
            vertices = [
                        [-3.,0.9],
                        [0.0,random_vertex]
                                ]
            wires = [wire(vertices[0],vertices[1],size=size)]

    #Produce the data for the contour plot.        
    print "\nGenerating Successful Magnetic Field {0}".format(Nconfig+1)
    for i in range(len(field)):
        sys.stdout.write('\rProgress: {0}%'.format(i*100/size+1))
        sys.stdout.flush()
        for j in range(len(field[0])):
            B_vector = np.array([B_bias,0.,0.])
            for k in wires:
                B_vector += k.B_vec([float(j),float(i),z])
            mod_B = np.sqrt(B_vector[0]**2 + B_vector[1]**2 + B_vector[2]**2)
            field[i][j] = mod_B
            
            if i == size/2:
                x_B_x[j] = B_vector[0]
                x_B_y[j] = B_vector[1]
                x_B_z[j] = B_vector[2]
                x_B[j] = mod_B
            if j == size/2:
                y_B_x[i] = B_vector[0]
                y_B_y[i] = B_vector[1]
                y_B_z[i] = B_vector[2]
                y_B[i] = mod_B




    ###############################################
    #######            Plotting             #######
    ###############################################
    plt.figure(figsize=(0.55*20,0.55*19))
    gs = gridspec.GridSpec(20, 19)
    plt.subplot(gs[:11,:11])

    #Generate contour plot.
    CS = plt.contourf(X, Y, field, 40,
                      cmap=plt.cm.gist_stern,
                      origin='lower')

    #Appropriate scaling.                  
    field += 0.1
    field[0][0] = 0

    #Create a custom title including all of the vertices.
    vertices_string = 'Magnetic field (B) above wire with vertices ($\\mu m$):'
    for i in range(len(vertices)):
        if not i % 9:
            vertices_string += '\n'
        v1 = round(size*vertices[i][0]-size/2.0,2)
        v2 = round(size*vertices[i][1]-size/2.0,2)
        vertices_string += '({0},{1}) '.format(v1,v2)
    vertices_string += '\nB-bias $\\vec{B} = %s$ $\\vec{e_x}$ $mT$, Wire Current $I= %s A$, Height: $ %s \\mu m $, Resolution: $ %s\\times %s $' % (round(B_bias,2),wires[0].I,round(z,2),size,size)
    plt.suptitle(vertices_string,size=9)
    plt.xlabel('$x$ ($\\mu m$)',size=10)
    plt.ylabel('$y$ ($\\mu m$)',size=10)

    #Contour plot.
    line = mlines.Line2D([size*row[0]-size/2.0 for row in vertices], [size*row[1]-size/2.0 for row in vertices], lw=3., alpha=0.3, color='k', linestyle='--')
    CS.ax.add_line(line)

    #B(x,y=0) profiles.
    plt.subplot(gs[12:14,:11])
    ax1 = plt.plot(X,x_B)
    plt.tick_params(axis='x',labelbottom='off')
    plt.tick_params(axis='y',which='both',labelsize=8)
    plt.ylabel('|$B$| ($mT$)',size=10)

    plt.subplot(gs[14:16,:11])
    ax2 = plt.plot(X,x_B_x)
    plt.tick_params(axis='x',labelbottom='off')
    plt.tick_params(axis='y',which='both',labelsize=8)
    plt.ylabel('$B_x$ ($mT$)',size=10)

    plt.subplot(gs[16:18,:11])
    ax3 = plt.plot(X,x_B_y)
    plt.tick_params(axis='x',labelbottom='off')
    plt.tick_params(axis='y',which='both',labelsize=8)
    plt.ylabel('$B_y$ ($mT$)',size=10)

    plt.subplot(gs[18:,:11])
    ax4 = plt.plot(X,x_B_z)
    plt.tick_params(axis='x',labelbottom='off')
    plt.tick_params(axis='y',which='both',labelsize=8)
    plt.ylabel('$B_z$ ($mT$)',size=10)
    plt.xlabel('Magnetic field at $y=0$')

    #B(x=0,y) profiles.
    ax1 = plt.subplot(gs[:11,11:13])
    plt.plot(y_B,Y)
    plt.tick_params(axis='y',labelleft='off')
    plt.tick_params(axis='x',which='both',labelsize=6)
    for label in ax1.axes.xaxis.get_ticklabels():
        label.set_rotation(90)
    plt.xlabel('|$B$| ($mT$)',size=10)

    ax2 = plt.subplot(gs[:11,13:15])
    plt.plot(y_B_x,Y)
    plt.tick_params(axis='y',labelleft='off')
    plt.tick_params(axis='x',which='both',labelsize=6)
    for label in ax2.axes.xaxis.get_ticklabels():
        label.set_rotation(90)
    plt.xlabel('$B_x$ ($mT$)',size=10)

    ax3 = plt.subplot(gs[:11,15:17])
    plt.plot(y_B_y,Y)
    plt.tick_params(axis='y',labelleft='off')
    plt.tick_params(axis='x',which='both',labelsize=6)
    for label in ax3.axes.xaxis.get_ticklabels():
        label.set_rotation(90)
    plt.xlabel('$B_y$ ($mT$)',size=10)

    ax4 = plt.subplot(gs[:11,17:])
    ax4.yaxis.set_label_position("right")
    plt.plot(y_B_z,Y)
    plt.tick_params(axis='y',labelleft='off')
    plt.tick_params(axis='x',which='both',labelsize=6)
    for label in ax4.axes.xaxis.get_ticklabels():
        label.set_rotation(90)
    plt.xlabel('$B_z$ ($mT$)',size=10)
    plt.ylabel('Magnetic field at $x=0$')

    #B(z) profile.
    plt.subplot(gs[13:,13:])
    plt.plot(Z,z_B)
    plt.xlabel('$z$, ($\\mu m$)')
    plt.ylabel('|$B$|, ($mT$)',size=10)
    cbar = plt.colorbar(CS)
    cbar.ax.set_ylabel('Magnetic field, $B$ ($mT$)')

    plt.savefig(os.path.join(directory,'magnetic_trap_{}.png'.format(Nconfig+1)))
    plt.close()