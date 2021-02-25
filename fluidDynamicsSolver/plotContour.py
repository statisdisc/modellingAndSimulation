def plotContour(x, y, z, filename, 
        cmap="bwr", 
        folder="", 
        xlim=[], 
        ylim=[], 
        title="", 
        xlabel="", 
        ylabel="", 
        levels=100, 
        vmin=0., 
        vmax=1.,
        hide_labels=True,
        equal_aspect_ratio=True):
    
    dpi = 200.
    if equal_aspect_ratio:
        fig = plt.figure()
    else:
        fig = plt.figure(figsize=(1000/dpi,1000/dpi), dpi=dpi)

    triang = tri.Triangulation(x, y)
    contours = plt.tricontourf(triang, z, levels, cmap=cmap, vmin=vmin, vmax=vmax)
    
    if xlim != []:
        plt.xlim(xlim)
    
    if ylim != []:
        plt.ylim(ylim)
        
    if hide_labels:
        plt.tick_params(axis='both', labelleft='off', labeltop='off', labelright='off', labelbottom='off')
        # plt.tick_params(axis='both', left='off', top='off', right='off', bottom='off', labelleft='off', labeltop='off', labelright='off', labelbottom='off')
        
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.suptitle(title)
    
    if equal_aspect_ratio:
        plt.gca().set_aspect("equal")
    fig.tight_layout()
    
    if folder == "":
        folder = sys.path[0]
    
    if equal_aspect_ratio:
        plt.savefig(os.path.join(folder, filename), dpi=dpi, bbox_inches="tight")
    else:
        plt.savefig(os.path.join(folder, filename), dpi=dpi)
    plt.close()