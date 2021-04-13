import numpy as np

#Calculate the magnetic field vector
def BVector(coords):
    B = np.zeros_like(coords)
    
    #Center B-field at this point.
    center = np.array([0.,0.,0.55])
    
    coordsB = coords.copy()
    coordsB[...] = coordsB[...] - center 
    
    d = 0.05                    #Diameter of Helmholtz coil, m. 
    s = 0.1                     #Separation of coils, m.
    mu_0 = 1.2566*10**(-6)      #Permearbility of free space.
    N = 50                      #Number of turns in coil.
    I = 1                       #Amps.
    # B_1 = 48*mu_0*N*I*d**2*s/(4*d**2+s**2)**(2.5)
    B_1 = 0.15                  #Tesla m^-1.
    
    B[...,0] = B_1 *  coordsB[...,0]/2.
    B[...,1] = B_1 *  coordsB[...,1]/2.
    B[...,2] = B_1 * -coordsB[...,2]
    
    return B

#Magnitude (absolute value) of magnetic field
def BMagnitude(coords):
    B = BVector(coords)
    BMag = np.sqrt( np.sum(B*B, axis=(B.ndim-1)) )
    return BMag
    
    
#Find the acceleration due to a light beam at a point vec{x}.
def acceleration(k, coords, I=1.0, factor=1.0):
    Delta = -2*np.pi*10**(7)                #Laser detuning, Hz.
    Gamma = 2*np.pi*6.067*10**(6)           #Natural linewidth.
    m = 1.443*10**(-25)                     #Atomic Mass of Rb 87.
    I_0 = 100                               #Intensity W m^-2.
    # I_0 = 500                             #Intensity W m^-2.
    I_s = 35.7                              #Saturation intensity W m^-2.    
    s_0 = I_0/I_s
    hbar = 6.63*10**(-34)/(2*np.pi)         #J s^-1 rad^-1.
    Lambda = 7.80241*10**(-7)               #m.
    mu_b = 9.274*10**(-24)                  #Bohr magneton.
    
    a_0 = I*hbar*Gamma*s_0*np.pi/(m*Lambda)
    B = BVector(coords)*0.01                            #Convert from cm to m.
    BMag = BMagnitude(coords)*0.01                        #Convert from cm to m.
    
    kB = np.sum(k*B, axis=(k.ndim-1))
    
    a_pi = 0.5*a_0*(1-(kB/BMag)**2)/(1+s_0+(2*Delta/Gamma)**2)
    a_sigmap = 0.25*a_0*(1-factor*(kB/BMag))**2/(1+s_0+(2*(Delta-mu_b*BMag/hbar)/Gamma)**2)
    a_sigmam = 0.25*a_0*(1+factor*(kB/BMag))**2/(1+s_0+(2*(Delta+mu_b*BMag/hbar)/Gamma)**2)
    
    a = (a_pi + a_sigmap + a_sigmam)[...,None]*k 
    return a