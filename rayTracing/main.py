import os
import sys
import random
import numpy as np
import scipy.misc
from src import surface
from src import ray
# execfile( os.path.join(os.path.join(os.path.dirname(os.path.realpath(__file__)), "src"), "surface.py") )
# execfile( os.path.join(os.path.join(os.path.dirname(os.path.realpath(__file__)), "src"), "ray.py") )


def main():
    
    mirror1 = surface.surface(vertices=[[0.,0.,0.], [0,1.,0.], [1.,1.,1.]], reflectivity=1.)
    mirror2 = surface.surface(vertices=[[0.,0.,0.], [1.,0.,1.], [1.,1.,1.]], reflectivity=0.5)
    
    screen = surface.surface(vertices=[[-2.,0.,0.], [-2.,10.,0.], [-2.,10.,10.]])
    
    resolution = 100
    image = np.zeros((resolution,resolution,3))
    nPhotons = 100000
    
    print "\nStarting ray-tracing"
    for i in xrange(nPhotons):
        sys.stdout.write("\rRay-tracing photon {} of {}__________".format(i+1, nPhotons))
        sys.stdout.flush()
        
        #Get light ray start coordinates and intensity based on coordinates
        x = random.random()
        y = random.random()
        intensity = np.exp(-((x-0.5)**2+(y-0.5)**2)/(2*0.01))/np.sqrt(2*np.pi*0.01)
        
        #Initialise light ray and calculate interaction (if any) with mirrors
        photon = ray.ray(origin=[x, y, 10.], direction=[0., 0., -1.], intensity=intensity)
        photon.origin, photon.direction, photon.intensity = mirror1.intersectPlane(photon.origin, photon.direction, photon.intensity)
        photon.origin, photon.direction, photon.intensity = mirror2.intersectPlane(photon.origin, photon.direction, photon.intensity)
        
        #See if light ray hits image screen
        intersectionPoint = screen.intersectionPoint(photon.origin, photon.direction)
        if (type(intersectionPoint) != bool):
            if (intersectionPoint[1] > 0.) and (intersectionPoint[1] < 1.):
                if (intersectionPoint[2] > 0.) and (intersectionPoint[2] < 1.):
                    index_y = int(resolution*intersectionPoint[1])
                    index_z = int(resolution*intersectionPoint[2])
                    image[index_z][index_y][:] += photon.intensity
        
    #Normalise image
    image *= 1./np.max(image)
    
    filename = os.path.join(os.path.dirname(os.path.realpath(__file__)), "rayTracedImage4.png")
    scipy.misc.toimage(image, cmin=0, cmax=1).save(filename)
        
if __name__ == "__main__":
    main()