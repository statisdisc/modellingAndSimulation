class cubeMesh2D:
    def __init__(
        self, 
        xmin=-1e4, xmax=1e4, dx=1e2, xPeriodic=False, 
        zmin=0e0, zmax=1e4, dz=1e2, zPeriodic=False
    ):
        
        self.xmin = xmin
        self.xmax = xmax
        self.dx = dx
        self.xPeriodic = xPeriodic
        
        self.dy = 1.

        self.zmin = zmin
        self.zmax = zmax
        self.dz = dz
        self.zPeriodic = zPeriodic

        self.xNCells = int(round( (xmax-xmin)/dx ))
        self.xCells = np.linspace(xmin+dx/2., xmax-dx/2., self.xNCells)
        self.xFaces = np.linspace(xmin, xmax-dx, self.xNCells)

        self.zNCells = int(round( (zmax-zmin)/dz ))
        self.zCells = np.linspace(zmin+dz/2., zmax-dz/2., self.zNCells)
        self.zFaces = np.linspace(zmin, zmax-dz, self.zNCells)
        
        #Construct empty cell-centred fields.
        self.volScalarField = np.zeros((self.zNCells, self.xNCells))
        self.volVectorField = np.zeros((self.zNCells, self.xNCells, 2))
        
        #Construct empty fields for cell faces
        self.surfaceScalarField = np.zeros((self.zNCells, self.xNCells))
        self.surfaceVectorField = np.zeros((self.zNCells, self.xNCells, 2))
        
        self.cellVolume = self.volScalarField.copy() + self.dx*self.dy*self.dz
        
        #Construct co-ordinate fields for cell centres
        self.x = self.volScalarField.copy()
        self.x[:,:] = self.xCells
        
        self.z = self.volScalarField.copy()
        for k in xrange(self.xNCells):
            self.z[:,k] = self.zCells[::-1]
        
        self.xz = self.volVectorField.copy()
        self.xz[:,:,0] = self.x
        self.xz[:,:,1] = self.z
        
        #Construct co-ordinate fields for cell faces
        self.xf = self.surfaceScalarField.copy()
        self.xf[:,:] = self.xFaces
        
        self.zf = self.surfaceScalarField.copy()
        for k in xrange(self.xNCells):
            self.zf[:,k] = self.zFaces[::-1]
        
        self.xzf = self.surfaceVectorField.copy()
        self.xzf[:,:,0] = self.x
        self.xzf[:,:,1] = self.zf
        
        self.xfz = self.surfaceVectorField.copy()
        self.xfz[:,:,0] = self.xf
        self.xfz[:,:,1] = self.z
        
        #Cell face, surface vector field
        self.xSf = self.surfaceVectorField.copy()
        self.xSf[:,:,0] += self.dy*self.dz
        
        self.zSf = self.surfaceVectorField.copy()
        self.zSf[:,:,1] += self.dx*self.dy