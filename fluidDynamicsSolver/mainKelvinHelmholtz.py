import os
import sys
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.tri as tri
import matplotlib.transforms as tr

execfile( os.path.join(sys.path[0], "runSettings.py") )
execfile( os.path.join(sys.path[0], "cubeMesh2D.py") )
execfile( os.path.join(sys.path[0], "finiteVolumeCalculations.py") )
execfile( os.path.join(sys.path[0], "fieldOperations.py") )
execfile( os.path.join(sys.path[0], "plotContour.py") )

dt = 0.1
tEnd = 1000.
mesh = cubeMesh2D(xPeriodic=True)
simulation = runSettings(dt=dt, tEnd=tEnd, plotInterval=tEnd/100.)
fvc = finiteVolumeFunctions(mesh)

x = mesh.x
z = mesh.z

#Constants
T = 300
R = 8.31
g = mesh.volVectorField.copy()
# g[:,:,1] = -9.81

#Velocity field
u = mesh.volVectorField.copy()
u += 10.
u[:49,:] = -10.
u[:51,50:150] = -10.

# u[:,50:150,0] = 10.
# for k in xrange(len(u)):
    # u[k,:,0] = 10*np.cos(np.pi/2. * mesh.xCells/10000.)**2

#Density field
rho = mesh.volScalarField.copy()
rho += 1.
# rho[:49,:] = 0.5
# rho[:51,50:150] = 0.5

tracer = mesh.volScalarField.copy()
tracer += 0.999
tracer[:49,:] = 0.
tracer[:51,50:150] = 0.

# plotContour(x.flatten(), z.flatten(), rho.flatten(), "z_rho_0.png", vmin=0.5)
plotContour(x.flatten(), z.flatten(), tracer.flatten(), "z_kh_0.png")
# plotContour(x.flatten(), z.flatten(), u[:,:,0].flatten(), "z_rho_0.png", vmin=0., vmax=15.)
while simulation.updateTime():
    sys.stdout.write("\rRunning simulation, t={}s".format(simulation.currentTime))
    sys.stdout.flush()
    
    pressure = rho*R*T
    rhoVec = mesh.volVectorField.copy()
    rhoVec[:,:,0] = rho
    rhoVec[:,:,1] = rho
    
    u = u - dt*fvc.uDotGradU(u, "upwind") + dt*g - dt*fvc.grad(pressure, "linear")/rhoVec
    
    rho = rho - dt*fvc.div(rho, u, "upwind")
    tracer = tracer - dt*fvc.div(tracer, u, "upwind")
    
    if simulation.plotFigures():
        print "\nPlotting profiles at t={}s".format(simulation.currentTime)
        fileId = "z_kh_{}.png".format(simulation.currentTimeIndex)
        # plotContour(x.flatten(), z.flatten(), rho.flatten(), fileId, vmin=0.5)
        plotContour(x.flatten(), z.flatten(), tracer.flatten(), fileId)
        # plotContour(x.flatten(), z.flatten(), u[:,:,0].flatten(), fileId, vmin=0., vmax=15.)
        
        # plt.figure()
        # plt.plot(x[50,:], u[50,:,0])
        # plt.ylim(0,15)
        # plt.savefig(os.path.join(sys.path[0], "z_test_{}.png".format(simulation.currentTimeIndex)))
        # plt.close()