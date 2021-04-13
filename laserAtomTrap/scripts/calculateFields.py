'''
Script for modelling the forces on neutral Rb-87 atoms in a magneto optical trap
with a single laser and reflection gratings.

WARNING
300MB of RAM recommended for resolution=100
10GB of RAM recommended for resolution=300
Resources scales as resolution^3
'''
import os
import sys
import time
import numpy as np

# User-made modules and functions
sys.path.append( os.path.dirname( os.path.dirname( os.path.abspath(__file__) ) ) )
from src.objects.folders import folders
from src.utilities.makeGrating import *
from src.utilities.physics import *


def calculateFields(
        id = "default",
        gratingType = "triangle",
        beamRadius = 1.2,
        gaussian = True,
        imperfection = False,
        resolution = 100,
        rangeX = [-0.55, 0.55],
        rangeY = [-0.55, 0.55],
        rangeZ = [0., 1.1],
        precisionCoords = 4,
        precisionData = 2
    ):
    '''
    Generate the acceleration and radiation profiles for a neutral atom in a 
    Magneto-Optical Trap with one laser pointed down on a horizontal surface where
    a reflection grating is located.
    
    Args
    id:               Data id used for the naming of output files
    gratingType:      Shape of grating etches/grooves. Valid parameters are "triangle" and "square"
    beamRadius:       The incident laser beam radius in cm.
    gaussian:         Is the beam profile Gaussian or uniform? Boolean only.
    imperfection:     If True, some of the laser beam will be diffracted to 0th order (reflection)
    resolution:       Resolution of the data in all 3 axes. resolution x 2 = computation x 8.
    rangeX:           Range of x values to be evaluated in cm.
    rangeY:           Range of x values to be evaluated in cm.
    rangeZ:           Range of x values to be evaluated in cm.
    precisionCoords:  Precision of coordinate data when writen to output file.
    precisionData:    Precision of field data when writen to output file.
    '''
    
    print(f"\nGenerating fields for configuration: {id}")
    
    folder = folders(
        id = id,
        folderScripts = os.path.dirname(os.path.realpath(__file__))
    )

    # Get grating geometry and properties
    if gratingType == "square":
        gratings = makeSquareGrating()
    elif gratingType == "triangle":
        gratings = makeTriangleGrating()
    else:
        gratings = makeSquareGrating()


    # 3D Coordinate and Acceleration vector fields.
    axisX = np.linspace(rangeX[0], rangeX[1], resolution)
    axisY = np.linspace(rangeY[0], rangeY[1], resolution)
    axisZ = np.linspace(rangeZ[0], rangeZ[1], resolution)
    z, y, x = np.meshgrid(axisZ, axisY, axisX, indexing='ij')
    coords = np.stack((x,y,z), axis=-1)

    # Data arrays
    a = np.zeros(coords.shape)
    radPressure = np.zeros(coords.shape)
    waveVector = np.zeros(coords.shape)


    print("Generating fields from incident beam")

    # Compute acceleration or radiation pressure from incident laser beam.
    intensity = np.ones(x.shape)
    if gaussian == True:
        intensity *= np.e**(-(x**2 + y**2)/2.)

    k = np.array([0., 0., -1.])
    waveVector[...] = k

    a += acceleration(waveVector, coords, I=intensity)
    radPressure[...] += intensity[...,None]*waveVector

    # Ignore regions not within the beam radius
    conditionBeam = x**2 + y**2 <= beamRadius**2
    a *= conditionBeam[...,None]
    radPressure *= conditionBeam[...,None]

    # Compute acceleration or radiation pressure from 0th order beam.
    if imperfection == True:
        print("Generating fields from 0th-order diffracted beam")
        
        intensity = 0.01
        if gaussian == True:
            intensity *= np.exp(-(0.5*x)**2)
        
        k = np.array([0., 0., 1.])
        waveVector[...] = k
        
        a += acceleration(waveVector, coords, I=intensity, factor=-1.)
        radPressure[...] += intensity[...,None]*waveVector

    switch = True
    for grating in gratings:
        print("Generating fields from grating segment")
        
        if switch == True:
            switch = False
            factor = -1
        else:
            factor = 1
        
        # Compute acceleration or radiation pressure from kth grating 1st order beam.
        intensity = grating.reflectivity * grating.intensity(
            coords, 
            factor, 
            beamRadius, 
            gaussian=gaussian
        )
        # Unit vector of diffracted beam
        waveVector[...] = grating.k
        radPressure += waveVector * intensity[...,None]
        a += acceleration(waveVector, coords, I=intensity, factor=-1.)
        
        # Compute acceleration or radiation pressure from kth grating 1st order beam in other direction.
        intensity = grating.reflectivity * grating.intensity(
            coords, 
            -factor, 
            beamRadius, 
            gaussian=gaussian
        )
        # Unit vector of diffracted beam
        waveVector[...] = grating.k
        radPressure += waveVector * intensity[...,None]
        a += acceleration(waveVector, coords, I=intensity, factor=-1.)

    # Store the acceleration magnitude and the components of the acceleration.
    aMag = np.sqrt(np.sum(a*a, axis=(a.ndim-1)))
    radPressureMag = np.sqrt(np.sum(radPressure*radPressure, axis=(radPressure.ndim-1)))
    
    # Save fields for future use
    np.savez_compressed(
        os.path.join(folder.outputs, "fieldData.npz"), 
        id = id,
        gratingType = gratingType,
        beamRadius = beamRadius,
        gaussian = gaussian,
        imperfection = imperfection,
        resolution = resolution,
        rangeX = rangeX,
        rangeY = rangeY,
        rangeZ = rangeZ,
        axisX = axisX,
        axisY = axisY,
        axisZ = axisZ,
        x = x.round(decimals=precisionCoords),
        y = y.round(decimals=precisionCoords),
        z = z.round(decimals=precisionCoords),
        a = a.round(decimals=precisionData),
        aMag = aMag.round(decimals=precisionData),
        radPressure = radPressure.round(decimals=precisionData),
        radPressureMag = radPressureMag.round(decimals=precisionData)
    )

    

if __name__ == "__main__":
    timeInit = time.time()
    
    calculateFields(id="triangleGaussian")
    calculateFields(id="triangle", gaussian=False)
    calculateFields(id="squareGaussian", gratingType="square")
    calculateFields(id="square", gratingType="square", gaussian=False)
    
    timeElapsed = time.time() - timeInit
    print(f"Elapsed time: {timeElapsed:.2f}s")