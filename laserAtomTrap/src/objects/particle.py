import numpy as np

class particle:
    # Initialising function. Declare variables.
    def __init__(self, position, velocity, dragCoefficient=0.):
        self.position = position
        self.velocity = velocity
        self.dragCoefficient = dragCoefficient
        
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
    
    def drag(self):
        '''
        Calculate the drag of the particle with respect to its frame of reference
        '''
        return -self.dragCoefficient * np.sqrt(np.dot(self.velocity,self.velocity)) * self.velocity
    
    def move(self, a, dt):
        '''
        Move the particle given an acceleration (a) and a timestep (dt)
        '''
        self.velocity = self.velocity + dt*a + dt*self.drag()
        self.position = self.position + dt*self.velocity
        
        self.addHistory()