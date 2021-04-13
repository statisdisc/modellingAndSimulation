import numpy as np

# Diffraction grating object which redirects light
class grating:
    mu_0 = 4 * np.pi * 10**(-7)                # Permeability of free space. m kg s^-2 A^-2.
    
    # Initialising function. Declare variables.
    def __init__(self, region, direction, theta, reflectivity):
        self.region = region                  #Array which defines the region on the x-y plane where the grating exists.
        self.direction = direction            #Direction in which the etches in the grating are.
        self.theta = theta                    #Angle of diffraction with respect to the z-axis.
        self.reflectivity = reflectivity      #Ratio of light which is diffracted to 1st order.
        
        if type(self.region) == list:
            self.region = np.array(self.region)
        
        if type(self.direction) == list:
            self.direction = np.array(self.direction)
        
    # Return relative intensity for a guassian beam hitting the grating at [x,y].
    def gaussianBeam(self, x, y, center=[0.,0.], intensity=1.):
        return intensity*np.e**(-((x-center[0])**2 + (y-center[1])**2)/2.)
        
    # For a coordinate [x,y,z], find the intensity of light received from this grating
    # by tracing back where the light may have originated from on the grating.
    def intensity(self, coords, factor, beam_radius, gaussian=False):
        # Calculate the direction of the wave vector k.
        # Direction will be perpendicular to the direction of the grating etches/grooves.
        x = -self.direction[1]*factor
        y =  self.direction[0]*factor
        z = np.sqrt(x**2 + y**2)*np.tan(self.theta)
        
        self.k = np.array([x,y,z])
        self.k /= np.sqrt(np.dot(self.k,self.k))
        
        # Find ratio of z-co-ordinate to z-component of k.
        # This is used to find the intersection of the vector with the grating plane.
        scaling = coords[...,2]/self.k[2]
        
        intersectionPoints = coords.copy()
        intersectionPoints[...,0] -= scaling * self.k[0]     #Intersection of the light with the grating.
        intersectionPoints[...,1] -= scaling * self.k[1]     #Intersection of the light with the grating.
        intersectionPoints[...,2] -= scaling * self.k[2]     #Intersection of the light with the grating.
        
        # If the intersection point is outside of the grating area, return 0 intensity.
        # I.E. This point in region does not receive light from this grating.
        intensity = np.ones(intersectionPoints[...,0].shape, dtype=bool)
        
        # Also return 0 intensity if intersection point is outside of beam radius (no diffraction).
        condition1 = intersectionPoints[...,0]**2 + intersectionPoints[...,1]**2 <= beam_radius**2
        
        intensity *= condition1
        
        for i in self.region:
            # If on chip surface: ax + by + c > 0, where i=[a,b,c].
            # If no beam from grating, return 0 intensity using boolean operations.
            condition2 = i[0]*intersectionPoints[...,0] + i[1]*intersectionPoints[...,1] + i[2] > 0     
            
            intensity *= condition2
        
        if gaussian:
            intensity = self.gaussianBeam(intersectionPoints[...,0], intersectionPoints[...,1])*intensity
        
        return intensity