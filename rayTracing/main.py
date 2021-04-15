import os
import sys
import random
import time
import numpy as np
from PIL import Image

# User-made modules and functions
from src import surface
from src import ray
# execfile( os.path.join(os.path.join(os.path.dirname(os.path.realpath(__file__)), "src"), "surface.py") )
# execfile( os.path.join(os.path.join(os.path.dirname(os.path.realpath(__file__)), "src"), "ray.py") )


def main():
    
    mirror1 = surface.surface(vertices=[[0.,0.,0.], [0,1.,0.], [1.,1.,1.]], reflectivity=1.)
    mirror2 = surface.surface(vertices=[[0.,0.,0.], [1.,0.,1.], [1.,1.,1.]], reflectivity=0.5)
    objects = [mirror1, mirror2]
    
    screen = surface.surface(vertices=[[-2.,0.,0.], [-2.,10.,0.], [-2.,10.,10.]])
    
    resolution = 100
    image = np.zeros((resolution,resolution,3))
    nPhotons = 1000000
    
    photonOrigin = np.zeros((nPhotons,3))
    photonOrigin[:,0] = np.random.rand(nPhotons)
    photonOrigin[:,1] = np.random.rand(nPhotons)
    photonOrigin[:,2] = 10.
    
    photonDirection = np.zeros((nPhotons,3))
    photonDirection[:,2] = -1.
    
    photonIntensity = np.exp(-((photonOrigin[:,0]-0.5)**2+(photonOrigin[:,1]-0.5)**2)/(2*0.01))/np.sqrt(2*np.pi*0.01)
    
    print("\nStarting ray-tracing")
    for object in objects:
        photonOrigin, photonDirection, photonIntensity = object.intersectSurface(photonOrigin, photonDirection, photonIntensity)
        
    #See if light ray hits image screen
    intersection = screen.intersect(photonOrigin, photonDirection)
    intersectionPoints, conditionIntersect = screen.intersectionPointOnPlane(photonOrigin, photonDirection)
    
    indexY = intersectionPoints[:,1]
    indexZ = intersectionPoints[:,2]
    condition = conditionIntersect*(indexY > 0.)*(indexY < 1.)*(indexZ > 0.)*(indexZ < 1.)
    
    
    if len(condition[condition]) > 0:
        indexY = resolution*indexY[condition]
        indexZ = resolution*indexZ[condition]
        intensity = photonIntensity[condition]
        
        image[indexZ.astype(int),indexY.astype(int)] = image[indexZ.astype(int),indexY.astype(int)] + photonIntensity[:,None]
        
    #Normalise image
    image /= np.max(image)
    
    filename = os.path.join(os.path.dirname(os.path.realpath(__file__)), "rayTracedImage.png")
    image = Image.fromarray( (255*image).astype(np.uint8) )
    image.save(filename)
        
if __name__ == "__main__":
    timeInit = time.time()
    main()
    timeElapsed = time.time() - timeInit
    print(f"\nElapsed time: {timeElapsed:.2f}s")