import numpy as np

#Diffraction grating object which redirects light
class grating:
    mu_0 = 4 * np.pi * 10**(-7)                #Permeability of free space. m kg s^-2 A^-2.
    
    #Initialising function. Declare variables.
    def __init__(self, space, direction, theta, diffraction_ratio):
        self.space = space                    #Array which defines the space on the x-y plane where the grating exists.
        self.dir = direction                  #Direction in which the etches in the grating are.
        self.theta = theta                    #Angle of diffraction with respect to the z-axis.
        self.ratio = diffraction_ratio        #Ratio of light which is diffracted to 1st order.
        
    #Return relative intensity for a guassian beam hitting the grating at [x,y].
    def gaussian_beam(self,x,y):
        return np.e**(-(x**2 + y**2)/2.)
        
    #For a point [x,y,z], find the intensity of light received from this grating.
    def intensity(self,pos,factor,beam_radius,gaussian=False):
        #Calculate the direction of the wave vector k.
        ##Direction will be perpendicular to the direction of the grating etches.
        x = -self.dir[1]*factor
        y = self.dir[0]*factor
        #Corresponding z and k_vector.
        z = np.sqrt(x**2 + y**2)*np.tan(self.theta)
        self.kvector = np.array([x,y,z])
        
        #Find ratio of z-co-ordinate to z-component of k.
        #This is used to find the intersection of the vector with the plane.
        ratio = abs(pos[2]/self.kvector[2])
        inter = -self.kvector*ratio            #Intersection of the light with the grating.
        inter[0] += pos[0]
        inter[1] += pos[1]
        
        #If the intersection point is outside of the grating area, return 0 intensity.
        #I.E. This point in space does not receive light from this grating.
        for i in self.space:
            #If on chip surface: ax + by + c > 0.
            if i[0]*inter[0] + i[1]*inter[1] + i[2] <= 0:
                return [0.,0.]                #No beam from grating, return 0 intensity.
            
            #Also return 0 intensity if intersection point is outside of beam radius (no diffraction).
            if inter[0]**2 + inter[1]**2 > beam_radius**2:
                return [0.,0.]
                
        # vertical_beam = self.ratio*np.sin(self.theta)
        # horizontal_beam = -np.sign(x)*self.ratio*np.cos(self.theta)
        vertical_beam = 1.
        horizontal_beam = 1.
        
        if gaussian == True:
            vertical_beam *= self.gaussian_beam(inter[0],inter[1])
            horizontal_beam *= self.gaussian_beam(inter[0],inter[1])
        
        return np.array([vertical_beam,horizontal_beam])