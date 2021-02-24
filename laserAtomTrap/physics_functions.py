import numpy as np

#Calculate the magnetic field vector
def B_vec(pos):
    #Center B-field at this point.
    center = np.array([0.,0.,0.55])
    pos = pos - center 
    
    d = 0.05                    #Diameter of Helmholtz coil, m. 
    s = 0.1                     #Separation of coils, m.
    mu_0 = 1.2566*10**(-6)      #Permearbility of free space.
    N = 50                      #Number of turns in coil.
    I = 1                       #Amps.
    # B_1 = 48*mu_0*N*I*d**2*s/(4*d**2+s**2)**(2.5)
    B_1 = 0.15                  #Tesla m^-1.
    
    B_field = B_1 * np.array([pos[0]/2.,pos[1]/2.,-pos[2]])
    return B_field

#Magnitude of magnetic field
def B_mag(pos):
    B_field = B_vec(pos)
    B = np.sqrt(np.dot(B_field,B_field))
    return B
    
    
#Find the acceleration due to a light beam at a point vec{x}.
def a(k,x,theta,I=1.0,factor=1.0):
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
    B = B_vec(x)*0.01                            #Convert from cm to m.
    mod_B = B_mag(x)*0.01                        #Convert from cm to m.
    
    a_pi = 0.5*a_0*(1-(np.dot(k,B)/mod_B)**2)/(1+s_0+(2*Delta/Gamma)**2)
    a_sigmap = 0.25*a_0*(1-factor*(np.dot(k,B)/mod_B))**2/(1+s_0+(2*(Delta-mu_b*mod_B/hbar)/Gamma)**2)
    a_sigmam = 0.25*a_0*(1+factor*(np.dot(k,B)/mod_B))**2/(1+s_0+(2*(Delta+mu_b*mod_B/hbar)/Gamma)**2)
    a = (a_pi+a_sigmap+a_sigmam)*k 
    return a