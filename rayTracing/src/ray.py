import numpy as np

class ray:
    def __init__(self, origin=[0., 0., 0.], direction=[1., 0., 0.], intensity=1.):
        self.origin = np.array([origin])
        self.direction = np.array([direction])
        self.intensity = np.array([intensity])