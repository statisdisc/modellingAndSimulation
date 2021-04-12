import numpy as np
from ..objects.grating import grating

''''''''''''''''''''''''''''''''''''
'''        Square Grating.       '''
''''''''''''''''''''''''''''''''''''
def makeSquareGrating():
    '''
    Square grating located on the x-y plane
    '''
    angle = np.pi/2. - 41 * np.pi / 180.0
    reflectivity = 1/(4.*np.cos(np.pi/2. - angle))
    
    ''' x > -1, x < 1, y > -1, y < 1 '''
    region = [[1,0,1.],[-1,0,1.],[0,1,1.],[0,-1,1.]]
    
    gratings = []
    gratings.append( grating(region, [1,0], angle, reflectivity) )
    gratings.append( grating(region, [0,1], angle, reflectivity) )
    
    return gratings


''''''''''''''''''''''''''''''''''''
'''        Triangular Grating.   '''
''''''''''''''''''''''''''''''''''''
def makeTriangleGrating():
    
    angle = np.pi/2. - 41 * np.pi / 180.0
    reflectivity = 1/(3.*np.cos(np.pi/2. - angle))
    
    tan60 = np.tan(60 * np.pi / 180.0)
    sin60 = np.sin(60 * np.pi / 180.0)
    cos60 = np.cos(60 * np.pi / 180.0)
    tan30 = np.tan(30 * np.pi / 180.0)
    sin30 = np.sin(30 * np.pi / 180.0)
    cos30 = np.cos(30 * np.pi / 180.0)
    
    '''Grating 1 dimensions.'''
    ''' x > -1.2, tan(60)*x + y < 0, -tan(60)*x + y > 0 '''
    region1 = [[1,0,1.2],[-tan60,-1,0.],[-tan60,1,0.]]
    '''Grating 3 dimensions.'''
    ''' tan(60)*x + y > 0, x < 1.2, y > 0, y < 1.2 '''
    region2 = [[tan60,1,0.],[-1,0,1.2],[0,1,0.],[0,-1,1.2]]
    '''Grating 2 dimensions.'''
    ''' tan(60)*x - y > 0, x < 1.2, y < 0, y > -1.2 '''
    region3 = [[tan60,-1,0.],[-1,0,1.2],[0,-1,0.],[0,1,1.2]]
    
    gratings = []
    gratings.append( grating(region1, [0,1], angle, reflectivity) )
    gratings.append( grating(region2, [-cos30,sin30], angle, reflectivity) )
    gratings.append( grating(region3, [ cos30,sin30], angle, reflectivity) )
    
    return gratings