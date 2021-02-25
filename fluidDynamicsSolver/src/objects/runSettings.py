class runSettings:
    def __init__(self, tStart=0., tEnd=1000., dt=1., writeInterval=0., plotInterval=0.):
        self.tStart = tStart
        self.tEnd = tEnd
        self.dt = dt
        self.currentTime = tStart
        self.currentTimeIndex = 0
        self.t = np.arange(tStart, tEnd, dt)
        
        self.writeInterval = writeInterval
        self.plotInterval = plotInterval
        
    def updateTime(self):
        self.currentTime += self.dt
        self.currentTimeIndex += 1
        return (self.currentTime <= self.tEnd)
    
    def plotFigures(self):
        return ((self.currentTime+dt/1000.)%self.plotInterval < dt/100.)