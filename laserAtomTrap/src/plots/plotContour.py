import os
import sys
import numpy as np
import matplotlib
# matplotlib.use("Agg")
import matplotlib.pyplot as plt

def plotContour(
        x, y, z,
        showMesh = False,
        id = "", 
        cmap = "hot",
        title = "", 
        xlabel = "",
        ylabel = "",
        ylabelCBar = "",
        xlim = [],
        ylim = [],
        dpi = 200,
        folder = "", 
        shading = [],
        u = [],
        v = [],
        vectorInterval = 35,
        vectorScale = 10
    ):
    
    fig, ax = plt.subplots(1,1,figsize=(8,6))
    
    # Plot regions where clouds exist (based on liquid water, ql)
    c = ax.pcolor(x, y, z, cmap=cmap, vmin=np.min(z), vmax=np.max(z), shading="auto")
    
    cBar = fig.colorbar(c, ax=ax)
    cBar.ax.set_ylabel(ylabelCBar)
    
    # Plot contours for some specified structure, given by the shading parameter
    if shading != []:
        X, Y = np.meshgrid(x, y)
        
        # Fill regions
        cmapShading = matplotlib.colors.LinearSegmentedColormap.from_list(
            "cmapShading", 
            [(0., 0., 0., 0.), (1., 0., 0., 0.5)]
        )
        ax.contourf(
            X, Y, shading, 2, 
            cmap=cmapShading, 
            vmin=np.min(shading), 
            vmax=1.1*np.max(shading), 
            linewidths=(0,0)
        )
        
        # Outline regions
        ax.contour(X, Y, shading, levels=[0.9], colors=[(1.,0.,0.)], linewidths=[1.])
        
    
    
    # Show velocity vectors
    if u != [] and v != []:
        X, Y = np.meshgrid(x, y)
        plt.quiver(
            np.concatenate(X)[::vectorInterval], 
            np.concatenate(Y)[::vectorInterval], 
            np.concatenate(u)[::vectorInterval], 
            np.concatenate(v)[::vectorInterval], 
            angles='xy', 
            color="#888888", 
            scale=vectorScale, 
            headwidth=2
        )
    
    if xlim == []:
        xlim = [np.min(x), np.max(x)]
    if ylim == []:
        ylim = [np.min(y), np.max(y)]
    
    # Limits and labels
    ax.set_xlim(xlim)
    ax.set_ylim(ylim)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    plt.title(title)
    
    # Ensure x and y axis are the same scale
    plt.gca().set_aspect("equal")
    
    plt.savefig(
        os.path.join(folder, "contour_{}.png".format(id)), 
        bbox_inches="tight", 
        dpi=dpi
    )
    plt.close()