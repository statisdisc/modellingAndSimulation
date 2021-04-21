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
    coords = np.stack((x,y,z), axis=-1)
    
    particles = []
    nParticles = 15
    for i in range(nParticles):
        # particles.append(
            # particle(
                # [
                    # random.uniform(data["axisX"][0], data["axisX"][-1]),
                    # random.uniform(data["axisY"][0], data["axisY"][-1]),
                    # random.uniform(data["axisZ"][0], data["axisZ"][-1])
                # ],
                # [0,0,0]
            # )
        # )
        particles.append(
            particle(
                [
                    0.5*random.uniform(data["axisX"][0], data["axisX"][-1]),
                    0.5*random.uniform(data["axisY"][0], data["axisY"][-1]),
                    0.25*random.uniform(data["axisZ"][0], data["axisZ"][-1])
                ],
                [0,0,0]
            )
        )
    
    timestep = 5e-4
    timesteps = 50
    for i in range(nParticles):
        print("Simulating trajectory of particle {}".format(i+1))
        for n in range(timesteps):
            # distance = np.abs(coords-particles[i].position)
            # indices = np.argmin(np.sum((coords-particles[i].position)**2, axis=-1), axis=-1)
            indexX = np.argmin(np.abs(data["axisX"]-particles[i].position[0]))
            indexY = np.argmin(np.abs(data["axisY"]-particles[i].position[1]))
            indexZ = np.argmin(np.abs(data["axisZ"]-particles[i].position[2]))
            
            a = data["a"][indexZ][indexX][indexY]
            
            particles[i].move(a, timestep)
    
    fig = plt.figure()
    ax = fig.gca(projection='3d')
    
    for i in range(nParticles):
        # print(particles[i].positions)
        pos = np.array(particles[i].positions)
        ax.plot(pos[...,0], pos[...,1], pos[...,2])
        # ax.plot(pos[...,0][::-1][::30], pos[...,1][::-1][::30], pos[...,2][::-1][::30], "k>")
        ax.plot(pos[...,0][-1], pos[...,1][-1], pos[...,2][-1], "ko")
    
    ax.set_xlim([data["axisX"][0], data["axisX"][-1]])
    ax.set_ylim([data["axisY"][0], data["axisY"][-1]])
    ax.set_zlim([data["axisZ"][0], data["axisZ"][-1]])
    
    ax.set_xlabel("x (cm)")
    ax.set_ylabel("y (cm)")
    ax.set_zlabel("z (cm)")
    
    plt.savefig(os.path.join(folder.outputs, "trajectories.png"), dpi=200)
    plt.close()

    

if __name__ == "__main__":
    timeInit = time.time()
    
    simulateAtoms(id="triangleGaussian")
    # simulateAtoms(id="triangle")
    # simulateAtoms(id="squareGaussian")
    # simulateAtoms(id="square")
    
    # simulateAtoms(id="triangleGaussianZoomOut")
    # simulateAtoms(id="triangleZoomOut")
    # simulateAtoms(id="squareGaussianZoomOut")
    # simulateAtoms(id="squareZoomOut")
    
    timeElapsed = time.time() - timeInit
    print(f"Elapsed time: {timeElapsed:.2f}s")