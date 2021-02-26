'''
Test case for modelling a Kelvin-Helmholtz instability which occurs when there
is a surface with wind shear either side of it.
'''
import os
import sys
import time
import numpy as np

# User-made modules
sys.path.append( os.path.dirname( os.path.dirname( os.path.abspath(__file__) ) ) )
from src.objects.folders import folders
from src.objects.cubeMesh2D import cubeMesh2D
from src.objects.finiteVolumeCalculations import finiteVolumeFunctions
from src.objects.runSettings import runSettings
from src.plots.plotContour import plotContour
from src.utilities.makeGif import makeGif
from src.utilities.fieldOperations import *

def main():
    # Fetch folders for code structure
    folder = folders( folderScripts=os.path.dirname(os.path.realpath(__file__)) )
    
    # Import the mesh for the fluid solver
    mesh = cubeMesh2D(xPeriodic=True)
    x = mesh.x
    z = mesh.z

    # Import finite volume operations using mesh geometry
    fvc = finiteVolumeFunctions(mesh)

    # Initialise the simulation
    simulation = runSettings(
        dt=0.01,                 # Timestep for simulation
        tEnd=1000,              # End time (s) of simulation
        plotInterval=10.        # Plot every [plotInterval] seconds
    )


    

    # Constants
    T = 300
    R = 8.31
    g = mesh.volVectorField.copy()
    # g[:,:,1] = -9.81
    
    
    '''
    INITIAL CONDITIONS
    '''
    # Velocity field
    u = mesh.volVectorField.copy()
    u += 10.
    u[:49,:] = -10.
    u[:51,50:150] = -10.

    # Density field
    rho = 0*mesh.volScalarField.copy() + 1

    tracer = mesh.volScalarField.copy()
    tracer += 0.999
    tracer[:49,:] = 0.001
    tracer[:51,50:150] = 0.001
    
    
    dt = simulation.dt

    # Plot initial conditions
    plotContour(x, z, tracer, "kelvinHelmholtz_0.png", folder=folder.outputs)
    
    # Run simulation until end time is reached
    while simulation.updateTime():
        sys.stdout.write("\rRunning simulation, t={}s".format(simulation.currentTime))
        sys.stdout.flush()
        
        pressure = rho*R*T
        
        # Continuity equation
        rho = rho - dt*fvc.div(rho, u, "upwind")
        rho = fvc.setBoundaryConditions(rho)
        
        # Momentum equation
        u = u - dt*fvc.uDotGradU(u, "upwind") + dt*g - dt*fvc.grad(pressure, "linear")/rho[:,:,None]
        u = fvc.setBoundaryConditions(u)
        
        # Advection of tracers which follow the flow
        tracer = tracer - dt*dot(u, fvc.grad(tracer, "upwind", u=u))
        
        if simulation.plotFigures():
            print "\nPlotting profiles at t={}s".format(simulation.currentTime)
            
            fileId = "kelvinHelmholtz_{}.png".format(simulation.currentTimeIndex)
            plotContour(x, z, tracer, fileId, folder=folder.outputs)
            
            # plotContour(x, z, rho, fileId, vmin=0.5, folder=folder.outputs)
            # plotContour(x, z, u[:,:,0], fileId, vmin=0., vmax=15., folder=folder.outputs)





if __name__ == "__main__":
    timeInit = time.time()
    main()
    timeElapsed = time.time()
    print "Elapsed time: {:.2f}s".format(timeElapsed-timeInit)