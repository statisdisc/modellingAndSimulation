'''
Script for plotting the forces on neutral Rb-87 atoms in a magneto optical trap
with a single laser and reflection gratings
'''
import os
import sys
import time
import random
import numpy as np

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

# User-made modules and functions
sys.path.append( os.path.dirname( os.path.dirname( os.path.abspath(__file__) ) ) )
from src.objects.folders import folders
from src.objects.particle import particle
from src.plots.plotContour import plotContour


def simulateAtoms(id="default"):
    '''
    Generate plots for the acceleration and radiation profiles for a neutral atom in a 
    Magneto-Optical Trap with one laser pointed down on a horizontal surface where
    a reflection grating is located.
    
    NOTE: plotContour must be run before using plotFields
    
    Args
    id:             Data id used for the input data filename and the output files
    '''
    
    print(f"\nPlotting fields for configuration: {id}")
    
    folder = folders(
        id = id,
        folderScripts = os.path.dirname(os.path.realpath(__file__))
    )

    
    # Save fields for future use
    data = np.load(os.path.join(folder.outputs, "fieldData.npz"))
    
    x = data["x"]
    y = data["y"]
    z = data["z"]
    a = data["a"]
    aMag = data["aMag"]
    axisX = data["axisX"]
    axisY = data["axisY"]
    axisZ = data["axisZ"]
    coords = np.stack((x,y,z), axis=-1)
    
    particles = []
    nParticles = 50
    for i in range(nParticles):
        # particles.append(
            # particle(
                # [
                    # random.uniform(data["axisX"][0], data["axisX"][-1]),
                    # random.uniform(data["axisY"][0], data["axisY"][-1]),
                    # random.uniform(data["axisZ"][0], data["axisZ"][-1])
                # ],
                # [0,0,0],
                # dragCoefficient = 10.
            # )
        # )
        particles.append(
            particle(
                [
                    0.5*random.uniform(data["axisX"][0], data["axisX"][-1]),
                    0.5*random.uniform(data["axisY"][0], data["axisY"][-1]),
                    random.uniform(data["axisZ"][0], data["axisZ"][-1])
                ],
                [0,0,0],
                dragCoefficient = 10.
            )
        )
    
    timestep = 5e-4
    timesteps = 500
    for i in range(nParticles):
        print("Simulating trajectory of particle {}".format(i+1))
        for n in range(timesteps):
            indexX = np.argmin(np.abs(axisX-particles[i].position[0]))
            indexY = np.argmin(np.abs(axisY-particles[i].position[1]))
            indexZ = np.argmin(np.abs(axisZ-particles[i].position[2]))
            
            acceleration = a[indexZ][indexY][indexX]
            
            particles[i].move(acceleration, timestep)
    
    
    # Generate 3D trajectory plots
    fig = plt.figure()
    ax = plt.axes(projection='3d')
    
    # Draw grating chip
    xGrating = [-1.,-1.,1.,1.]
    yGrating = [-1.,1.,1.,-1.]
    zGrating = [0.,0.,0.,0.]
    verts = [list(zip(xGrating,yGrating,zGrating))]
    poly = Poly3DCollection(verts, facecolors=[[0.5,0.5,0.5,1.]])
    poly.set_sort_zpos(50)
    ax.add_collection3d(poly)
    
    # Draw laser radius
    theta = np.linspace(0, 2 * np.pi, 100)
    radius = 1.2
    xLaser = radius * np.cos(theta)
    yLaser = radius * np.sin(theta)
    zLaser = np.zeros_like(xLaser)+0.01
    verts = [list(zip(xLaser,yLaser,zLaser))]
    poly = Poly3DCollection(verts, facecolors=[[1.,0.,0.,0.5]])
    poly.set_sort_zpos(100)
    ax.add_collection3d(poly)
    
    # Highlight region with weakest force-field (where particles should converge to)
    # cutOff = np.min(aMag) + 0.01*(np.mean(aMag)-np.min(aMag))
    # condition = aMag < cutOff
    # ax.plot(x[condition], y[condition], z[condition], ".", color="#888888")
    
    for i in range(nParticles):
        pos = np.array(particles[i].positions)
        zorder = 10000
        
        # Deal with particles that have gone through the ground
        if np.min(pos[:,2]) < 0.:
            pos[:,2] = np.maximum(pos[:,2], 0*pos[:,2])
        
        ax.plot(pos[...,0], pos[...,1], pos[...,2], zorder=zorder)
        ax.plot(pos[...,0][-1], pos[...,1][-1], pos[...,2][-1], "ko", zorder=zorder)
    
    ax.set_xlim([axisX[0], axisX[-1]])
    ax.set_ylim([axisY[0], axisY[-1]])
    ax.set_zlim([axisZ[0], axisZ[-1]])
    
    ax.set_xlabel("x (cm)")
    ax.set_ylabel("y (cm)")
    ax.set_zlabel("z (cm)")
    
    for i in np.linspace(0,1,25):
        elevation = 90*i
        angle = 90+360*i
        ax.view_init(elev=elevation, azim=angle)
        plt.savefig(os.path.join(folder.outputs, "trajectories_{}_{}.png".format(id, int(360*i))), dpi=200)
    plt.close()

    

if __name__ == "__main__":
    timeInit = time.time()
    
    simulateAtoms(id="triangleGaussian")
    simulateAtoms(id="triangle")
    simulateAtoms(id="squareGaussian")
    simulateAtoms(id="square")
    
    simulateAtoms(id="triangleGaussianZoomOut")
    simulateAtoms(id="triangleZoomOut")
    simulateAtoms(id="squareGaussianZoomOut")
    simulateAtoms(id="squareZoomOut")
    
    timeElapsed = time.time() - timeInit
    print(f"Elapsed time: {timeElapsed:.2f}s")