'''
Script for modelling and plotting the forces on neutral Rb-87 atoms in a magneto optical trap
with a single laser and reflection gratings.

If modelling the fields (computationally expensive) has been done previously, use
plotFields.py instead for faster computation.
Use this script if generating the data for the first time.

!---WARNING---!
300MB of RAM recommended for resolution=100
10GB of RAM recommended for resolution=300
Resources scales as resolution^3
'''
import os
import sys
import time
import numpy as np

# User-made modules and functions
from calculateFields import calculateFields
from plotFields import plotFields


def main(
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
    
    print(f"\nProcessin {id}")
    
    # Calculate the acceleration and radiation pressure, save to file in root/outputs/id/
    calculateFields(
        id = id,
        gratingType = gratingType,
        beamRadius = beamRadius,
        gaussian = gaussian,
        imperfection = imperfection,
        resolution = resolution,
        rangeX = rangeX,
        rangeY = rangeY,
        rangeZ = rangeZ,
        precisionCoords = precisionCoords,
        precisionData = precisionData
    )
    
    # Plot fields and save to root/outputs/id/
    plotFields(id=id)

    

if __name__ == "__main__":
    timeInit = time.time()
    
    main(id="triangleGaussian")
    main(id="triangle", gaussian=False)
    main(id="squareGaussian", gratingType="square")
    main(id="square", gratingType="square", gaussian=False)
    
    main(id="triangleGaussianZoomOut", rangeX = [-1.55, 1.55], rangeY = [-1.55, 1.55], rangeZ = [0., 3.1])
    main(id="triangleZoomOut", gaussian=False, rangeX = [-1.55, 1.55], rangeY = [-1.55, 1.55], rangeZ = [0., 3.1])
    main(id="squareGaussianZoomOut", gratingType="square", rangeX = [-1.55, 1.55], rangeY = [-1.55, 1.55], rangeZ = [0., 3.1])
    main(id="squareZoomOut", gratingType="square", gaussian=False, rangeX = [-1.55, 1.55], rangeY = [-1.55, 1.55], rangeZ = [0., 3.1])
    
    timeElapsed = time.time() - timeInit
    print(f"Elapsed time: {timeElapsed:.2f}s")