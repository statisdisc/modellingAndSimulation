'''
Script for plotting the forces on neutral Rb-87 atoms in a magneto optical trap
with a single laser and reflection gratings
'''
import os
import sys
import time
import numpy as np


# User-made modules and functions
sys.path.append( os.path.dirname( os.path.dirname( os.path.abspath(__file__) ) ) )
from src.objects.folders import folders
from src.plots.plotContour import plotContour


def plotFields(id="default"):
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
    
    
    slices = {}
    slices["XZ"] = {
        "xAxis": "x",
        "yAxis": "z",
        "xIndex": 0,
        "yIndex": 2,
        "location": "y = {:.2f} cm".format(data["axisY"][int(data["resolution"]/2)]),
        "slice": np.s_[:, int(data["resolution"]/2), :]
    }
    slices["YZ"] = {
        "xAxis": "y",
        "yAxis": "z",
        "xIndex": 1,
        "yIndex": 2,
        "location": "x = {:.2f} cm".format(data["axisX"][int(data["resolution"]/2)]),
        "slice": np.s_[:, :, int(data["resolution"]/2)]
    }
    slices["XY"] = {
        "xAxis": "x",
        "yAxis": "y",
        "xIndex": 0,
        "yIndex": 1,
        "location": "z = {:.2f} cm".format(data["axisZ"][int(data["resolution"]/2)]),
        "slice": np.s_[int(data["resolution"]/2), :, :]
    }
    
    
    for slice in slices:
        print("Plotting data for slice {}".format(slice))
        s = slices[slice]
        
        plotContour(
            data["axis"+s["xAxis"].upper()], 
            data["axis"+s["yAxis"].upper()], 
            data["radPressureMag"][s["slice"]], 
            id=id+"_radPressure_"+slice.lower(), 
            folder=folder.outputs,
            xlabel="{} (cm)".format(s["xAxis"]),
            ylabel="{} (cm)".format(s["yAxis"]),
            ylabelCBar="Relative radiation pressure",
            title="Radiation pressure field, {}".format(s["location"]),
            u = data["radPressure"][s["slice"]][...,s["xIndex"]],
            v = data["radPressure"][s["slice"]][...,s["yIndex"]],
            vectorScale = 10
        )
        
        plotContour(
            data["axis"+s["xAxis"].upper()], 
            data["axis"+s["yAxis"].upper()], 
            data["aMag"][s["slice"]], 
            id=id+"_a_"+slice.lower(), 
            folder=folder.outputs,
            cmap="jet_r",
            xlabel="{} (cm)".format(s["xAxis"]),
            ylabel="{} (cm)".format(s["yAxis"]),
            ylabelCBar="Relative acceleration",
            title="Acceleration field, {}".format(s["location"]),
            u = data["a"][s["slice"]][...,s["xIndex"]],
            v = data["a"][s["slice"]][...,s["yIndex"]],
            vectorScale = 2e5
        )

    

if __name__ == "__main__":
    timeInit = time.time()
    
    plotFields(id="triangleGaussian")
    plotFields(id="triangle")
    plotFields(id="squareGaussian")
    plotFields(id="square")
    
    plotFields(id="triangleGaussianZoomOut")
    plotFields(id="triangleZoomOut")
    plotFields(id="squareGaussianZoomOut")
    plotFields(id="squareZoomOut")
    
    timeElapsed = time.time() - timeInit
    print(f"Elapsed time: {timeElapsed:.2f}s")