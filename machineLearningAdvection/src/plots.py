#Plot the advection outputs for the ftbs scheme (y_ftbs) and machine learning scheme (y_obtained)
def plot_advection(x, y_init, y_obtained, y_ftbs, u, dt, filename="test"):
    
    dx = x[1]-x[0]
    x_init = x.copy()
    x_fini = x_init + u*dt

    #Shift ftbs and machine learning outputs to account for periodic boundary conditions.
    y_init = y_init.copy()
    y_ftbs = np.roll(y_ftbs, int(u*dt/dx))
    y_obtained = np.roll(y_obtained, int(u*dt/dx))
    
    plt.figure(figsize=(10,3))
    
    #Boundaries
    plt.plot([-1e3, 1e3], [0.,0.], ":", color="#999999")
    plt.plot([-1e3, 1e3], [1.,1.], ":", color="#999999")
    
    #Initial conditions
    plt.plot(x_init, y_init, "-", color="k")
    plt.plot(x_init, y_init, ".", color="k")
    
    #Analytic solution
    plt.plot(x_fini, y_init, "-", color="k")
    plt.plot(x_fini, y_init, ".", color="k")
    
    #FTBS advection scheme
    if dt > 0.:
        plt.plot(x_fini, y_ftbs, "-", color="b", alpha=0.5)
        plt.plot(x_fini, y_ftbs, ".", color="b", alpha=0.5)
    
    #Machine learning solution
    if dt > 0.:
        plt.plot(x_fini, y_obtained, "-", color="r", linewidth=2.)
        plt.plot(x_fini, y_obtained, "o", color="r")
    
    #Arrow to label movement
    x_start = x_init[np.argmax(y_init)]
    y_start = np.max(y_init)
    if u*dt > 0.:
        plt.arrow(x_start, y_start, u*dt, 0., length_includes_head=True, color="k")
    
    plt.xlim(0., 1.)
    plt.ylim(-0.05,1.05)
    
    # plt.suptitle("Advection of 1D profile", fontsize=15)
    plt.title("Advection of 1D profile, Time: $t$={:.2f}s, Velocity: $u$={:.2f}m/s, Displacement: {:.2f}m".format(dt, u, (u*dt)), fontsize=14)
    plt.xlabel("$x$ (m)")
    plt.ylabel("Profiles, $f(x)$")
    
    plt.savefig( os.path.join( os.path.dirname(os.path.realpath(__file__)), "plot_{}.png".format(filename) ), bbox_inches="tight", dpi=200 )
    plt.close()
    

#Generate a series of plots with different timesteps for a given set of initial conditions
def plot_all_simulations(test_data):

    x = np.linspace(0.,0.25,41)[:-1]
    dx = x[1]-x[0]
    
    t = np.linspace(0., 1., 21)
    dt = t[1]-t[0]
    
    #Store image filenames for animations
    image_files = []
    
    #Take each set of initial conditions (test_data[i]), run them for up to 1 second
    for i in xrange(len(test_data)):
        print "Plotting simulation {}".format(i+1)
        image_files.append([])
        
        #Get initial conditions and initialise solution fields
        y_init = test_data[i][0][2:,0]
        y_output = y_init.copy()
        y_ftbs = y_init.copy()
        
        #Force the velocity to be 0.75 m/s (so solution travels length of domain)
        # u = test_data[i][0][0][0]
        u = 0.75
        test_data[i][0][0][0] = u
        
        for n in xrange(len(t)):
            
            #Set the timestep for the machine learning simulation.
            # time = test_data[i][0][1][0]
            time = t[n]
            test_data[i][0][1][0] = time
            
            #Machine learning output
            y_output =  advect.feedforward( test_data[i][0] )[:,0]
            
            #Plot the ftbs and machine learning outputs
            filename = "sim_{}_t_{}".format(i+1, n)
            image_files[i].append( os.path.join( os.path.dirname(os.path.realpath(__file__)), "plot_{}.png".format(filename) ) )
            plot_advection(x, y_init, y_output, y_ftbs, u, time, filename=filename)
            
            #Advect ftbs scheme with sub-timesteps so Courant number is less than 1 and scheme is stable.
            for j in xrange(12):
                y_ftbs = ftbs(y_ftbs, u, dt/12., dx)

    return image_files
    

    
#Required imagemagick to be installed. If running on linux, use convert instead of magick convert.
def make_gif(filename, files, delay=5, loop=0):
    console = "magick convert -delay {} ".format(delay)
    for file in files:
        console += file + " "
    
    console += "-loop {} {}".format(loop, filename)
    
    os.system(console)
    
def delete_files(files):
    for file in files:
        os.remove( file )