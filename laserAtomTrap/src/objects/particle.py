import numpy as np

class particle:
    # Initialising function. Declare variables.
    def __init__(self, position, velocity):
        self.position = position
        self.velocity = velocity
        
        self.positions = []
        self.velocities = []
        
        if type(self.position) == list:
            self.position = np.array(self.position)
        
        if type(self.velocity) == list:
            self.velocity = np.array(self.velocity)
    
    def addHistory(self):
        self.positions.append(self.position)
        self.velocities.append(self.velocity)
    
    def update(self, position, velocity):
        '''
        Update particle properties
        '''
        self.position = position
        self.velocity = velocity
        
        self.addHistory()
    
    def move(self, a, dt):
        '''
        Move the particle given an acceleration (a) and a timestep (dt)
        '''
        self.velocity = self.velocity + dt*a
        self.position = self.position + dt*self.velocity
        
        self.addHistory()