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

dt = 0.01
tEnd = 20.
mesh = cubeMesh2D(xPeriodic=True, dx=1e3, dz=1e3)
# mesh = cubeMesh2D(xPeriodic=True)
simulation = runSettings(dt=dt, tEnd=tEnd, plotInterval=tEnd/200.)
fvc = finiteVolumeFunctions(mesh)

x = mesh.x
z = mesh.z

#Constants
theta = 300
p0 = 10**5
R = 8.31
gamma = 0.286
g = mesh.volVectorField.copy()
g[:,:,1] = -9.81
ones = mesh.volScalarField.copy() + 1
onesVec = mesh.volVectorField.copy() + 1

#Velocity field
u = mesh.volVectorField.copy()

#Density field
rho = mesh.volScalarField.copy()
# rho += 1.
# rho[:49,:] = 0.5
# rho[:51,50:150] = 0.5
rho += 0.5
rho[:len(rho)/2-1,:] = 1.
rho[:len(rho)/2+1,len(rho[0])/4:3*len(rho[0])/4] = 1.

tracer = mesh.volScalarField.copy()
tracer += 0.999
tracer[:len(rho)/2-1,:] = 0.
tracer[:len(rho)/2+1,len(rho[0])/4:3*len(rho[0])/4] = 0.

#Pressure field
pressure = p0 + rho*g[:,:,1]*z
pressureOld = p0 + rho*g[:,:,1]*z
pressure *= 0.

# print g[:,50,1] - fvc.grad(pressure, "linear")[:,50,1]/rho[:,50]


plotContour(x.flatten(), z.flatten(), rho.flatten(), "z_rho_0.png", vmin=0.5)
# plotContour(x.flatten(), z.flatten(), tracer.flatten(), "z_rt_0.png")
# plotContour(x.flatten(), z.flatten(), u[:,:,0].flatten(), "z_rho_0.png", vmin=0., vmax=15.)
while simulation.updateTime():
    sys.stdout.write("\rRunning simulation, t={}s__________".format(simulation.currentTime))
    sys.stdout.flush()
    
    # pressure = rho*R*theta
    # pressure = ( rho*R*theta/p0**gamma )**(1./(1.-gamma))
    # rhoVec = mesh.volVectorField.copy()
    # rhoVec[:,:,0] = rho
    # rhoVec[:,:,1] = rho
    
    uGradU = fvc.uDotGradU(u, "upwind")
    # pressure = rho*fvc.poissonSolver(pressure, -fvc.div(ones, uGradU, "linear"))
    pressure = rho*fvc.poissonSolver(pressure, -fvc.div(ones, u, "linear"))
    # u = u - dt*fvc.uDotGradU(u, "upwind") + dt*g - dt*fvc.grad(pressure, "linear")/rhoVec
    u = u - dt*uGradU + dt*g - dt*fvc.grad(pressure/rho, "linear")
    
    rho = rho - dt*fvc.div(rho, u, "upwind")
    tracer = tracer - dt*fvc.div(tracer, u, "upwind")
    
    
    
    
    # pressureNew = 2*pressure - pressureOld + (2*dt)**2 * pressure/rho * fvc.laplacian(pressure) + (2*dt)**2 * rho * fvc.div(ones, fvc.uDotGradU(u, "upwind"), "linear")
    # pressureNew = 2*pressure - pressureOld + (2*dt)**2 * pressure/rho * fvc.laplacian(pressure) + 100*(2*dt)**2 * rho * fvc.div(ones, u, "linear")
    # pressureNew = 2*pressure - pressureOld + (2*dt)**2 * rho * fvc.div(ones, u, "linear")
    # pressureOld = pressure.copy()
    # pressure = pressureNew.copy()
    
    if simulation.plotFigures():
        print "\nPlotting profiles at t={}s".format(simulation.currentTime)
        fileId = "z_rt_{}.png".format(simulation.currentTimeIndex)
        plotContour(x.flatten(), z.flatten(), rho.flatten(), fileId, vmin=0.5)
        # plotContour(x.flatten(), z.flatten(), tracer.flatten(), fileId)
        # plotContour(x.flatten(), z.flatten(), u[:,:,0].flatten(), fileId, vmin=0., vmax=15.)
        
        # plt.figure()
        # plt.plot(z[:,50], rho[:,50])
        # plt.plot(z[:,50], u[:,50,1])
        # plt.ylim(0,15)
        # plt.savefig(os.path.join(sys.path[0], "z_test_{}.png".format(simulation.currentTimeIndex)))
        # plt.close()