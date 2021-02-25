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

dt = 1.
mesh = cubeMesh2D(xPeriodic=True)
simulation = runSettings(dt=dt, tEnd=500., plotInterval=50)
fvc = finiteVolumeFunctions(mesh)

x = mesh.x
z = mesh.z

'''
Simple simulation with 2D square wave moved by uniform velocity field.
'''
u = mesh.volVectorField.copy()
# u[:,:,0] -= 10.
u[:,:,1] -= 10.

tracer = mesh.volScalarField.copy()
# tracer[:,80:120] += 0.999
tracer[40:60,:] += 0.999

plotContour(x.flatten(), z.flatten(), tracer.flatten(), "tracer_0.png")
while simulation.updateTime():
    sys.stdout.write("\rRunning simulation, t={}s".format(simulation.currentTime))
    sys.stdout.flush()
    tracer = tracer - dt*fvc.div(tracer, u, "upwind")
    # tracer = tracer - dt*dot(u, fvc.grad(tracer, "upwind", u=u))
    
    if simulation.plotFigures():
        print "\nPlotting profiles at t={}s".format(simulation.currentTime)
        fileId = "tracer_{}.png".format(simulation.currentTimeIndex)
        plotContour(x.flatten(), z.flatten(), tracer.flatten(), fileId)