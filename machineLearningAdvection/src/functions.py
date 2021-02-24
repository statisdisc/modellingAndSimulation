# Foward-in-time, Backwards-in-space advection scheme
def ftbs(y, u, dt, dx):
    return y - u*dt/dx * (y - np.roll(y,-1))
    
    
    
#Function for the inverse of sigmoid from network2py
def sigmoid_inverse(z):
    return -np.log(1./z - 1.)
    
    
    
#Basic square wave function with minimum 0 and maximum 1
def square_wave(x):
    y = 0*x
    y[len(x)/4:3*len(x)/4] += 1.
    return y
    
    
    
#Generate a superposition of wavemodes
def generate_modes(x, xmax, modes, amplitudes, phases):
    y = np.zeros(len(x))
    
    for i in xrange(len(modes)):
        # y += amplitudes[i] * np.sin( modes[i]*2*np.pi * (x - phases[i])/xmax )
        y += np.sin( modes[i]*2*np.pi * (x - phases[i])/xmax )
        
    #Ensure y in between 0 and 1
    y_min = np.min(y)
    y_max = np.max(y)
    y -= y_min 
    y *= 1./(y_max-y_min)
        
    return y

    
    
#Create a single data set including the initial conditions and the analytic solution.
def add_simulation(n_modes, square=False):
    
    #x domain in range [0,0.25]. This simplifies things when advecting beyond 0.25 (but below 1)
    nx = 40
    xmax = 0.25
    x = np.linspace(0.,xmax,nx+1)[:-1]
    
    #Randomise the (uniform) velocity and timestep
    u = random.uniform(0., 1.)
    dt = random.uniform(0., 1.)
    
    #Randomly generate the wave modes
    modes = np.linspace(0,n_modes,n_modes+1)
    mode_amplitudes = np.array([random.uniform(-1, 1) for i in range(n_modes+1)])
    mode_phases = np.array([random.uniform(-1, 1) for i in range(n_modes+1)])
    mode_info = (modes, mode_amplitudes, mode_phases)
    
    #Set input array for neural network array.
    #Unfortunately network2.py is set up to accept arrays of the form
    #[[0.1],
    #[0.2],
    #...
    #[0.8]]
    #instead of [0.1, 0.2, ... 0.8].
    input = np.zeros((nx+2, 1))
    input[0][0] = u
    input[1][0] = dt
    
    #Only use sigmoid function if initial conditions beyond [0,1], but convergence to solution may be slower.
    # input[2:,0] = sigmoid( generate_modes(x, xmax, modes, mode_amplitudes, mode_phases) )
    if square == True:
        input[2:,0] = square_wave(x)
    else:
        input[2:,0] = generate_modes(x, xmax, modes, mode_amplitudes, mode_phases)
    
    #Set analytic solution
    output = np.zeros((nx, 1))
    output[:,0] = generate_modes(x, xmax, modes, mode_amplitudes, mode_phases - u*dt)
    
    return (input, output), mode_info

    
    
#Create n_data sets of training data with maximum wavemodes n_modes.
#For a sine/cosine wave, use n_modes of 1.
def create_data_set(n_data, n_modes, square=False):
    
    training_data = []
    
    for i in xrange(n_data):
        sim_data, mode_info = add_simulation(n_modes, square=square)
        training_data.append( sim_data )
    
    return training_data
    

    
def simulation_error( data, truth ):
    return np.sum( (data-truth)**2 )
