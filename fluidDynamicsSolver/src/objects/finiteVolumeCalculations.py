import numpy as np
from ..utilities.fieldOperations import *

class finiteVolumeFunctions:
    def __init__(self, mesh):
        self.mesh = mesh
        self.small = self.mesh.volScalarField + 1e-16
    
    def gradComponents(self, field):
        gradxField = self.mesh.surfaceScalarField.copy()
        gradxField[:,:] = (field - np.roll(field, 1, axis=1))/self.mesh.dx
        if not self.mesh.xPeriodic:
            gradxField[:,0] *= 0.
        
        gradzField = self.mesh.surfaceScalarField.copy()
        gradzField[:,:] = (field - np.roll(field, -1, axis=0))/self.mesh.dz
        if not self.mesh.zPeriodic:
            gradzField[-1,:] *= 0.
        
        return gradxField, gradzField
    
    def grad(self, field, scheme, u=[]):
        gradField = self.mesh.volVectorField.copy()
        gradxField, gradzField = self.gradComponents(field)
        
        if scheme == "linear" or u == []:
            gradField[:,:,0] = 0.5*gradxField + 0.5*np.roll(gradxField, -1, axis=1)
            gradField[:,:,1] = 0.5*gradzField + 0.5*np.roll(gradzField,  1, axis=0)
        elif scheme == "upwind":
            ux = u[:,:,0]
            magUx = np.abs(ux)
            uxFactor = 0.5*(ux+magUx)/np.maximum(magUx, self.small)
            gradField[:,:,0] = uxFactor*gradxField + (1.-uxFactor)*np.roll(gradxField, -1, axis=1)
            
            uz = u[:,:,1]
            magUz = np.abs(uz)
            uzFactor = 0.5*(uz+magUz)/np.maximum(magUz, self.small)
            gradField[:,:,1] = uzFactor*gradzField + (1.-uzFactor)*np.roll(gradzField,  1, axis=0)
            
        gradField[0,:,1] = 0
        gradField[-1,:,1] = 0
        
        return gradField
    
    def uDotGradU(self, u, scheme):
        uGradU = self.mesh.volVectorField.copy()
        
        ux = u[:,:,0]
        uz = u[:,:,1]
        
        gradUx = self.grad(ux, scheme, u=u)
        gradUz = self.grad(uz, scheme, u=u)
        
        uGradU[:,:,0] = dot(u, gradUx)
        uGradU[:,:,1] = dot(u, gradUz)
        
        return uGradU
        
    def interpolateLinear(self, field):
        xField = self.mesh.surfaceScalarField.copy()
        xField[:,:] = 0.5*(field + np.roll(field, 1, axis=1))
        # if not self.mesh.xPeriodic:
            # xField[:,0] *= 0.
        
        zField = self.mesh.surfaceScalarField.copy()
        zField[:,:] = 0.5*(field + np.roll(field, -1, axis=0))
        # if not self.mesh.zPeriodic:
            # zField[-1,:] *= 0.
        
        return xField, zField
        
    def interpolateUpwind(self, field, u):
        
        ux = u[:,:,0]
        magUx = np.abs(ux)
        uxFactor = 0.5*np.abs(ux-magUx)/np.maximum(magUx, self.small)
        
        xField = self.mesh.surfaceScalarField.copy()
        xField[:,:] = uxFactor*field + (1.-uxFactor)*np.roll(field, 1, axis=1)
        # if not self.mesh.xPeriodic:
            # xField[:,0] *= 0.
        
        uz = u[:,:,1]
        magUz = np.abs(uz)
        uzFactor = 0.5*np.abs(uz-magUz)/np.maximum(magUz, self.small)
        
        zField = self.mesh.surfaceScalarField.copy()
        zField[:,:] = uzFactor*field + (1.-uzFactor)*np.roll(field, -1, axis=0)
        # if not self.mesh.zPeriodic:
            # zField[-1,:] *= 0.
        
        return xField, zField
    
    def div(self, field, u, scheme):
        divField = self.mesh.volScalarField.copy()
        
        if scheme == "upwind":
            fieldFacex, fieldFacez = self.interpolateUpwind(field, u)
        else:
            fieldFacex, fieldFacez = self.interpolateLinear(field)
        
        ux = u[:,:,0]
        uz = u[:,:,1]
        uFacex = u.copy()
        uFacez = u.copy()
        
        uxFacex, uxFacez = self.interpolateLinear(ux)
        uzFacex, uzFacez = self.interpolateLinear(uz)
        
        uFacex[:,:,0] = uxFacex
        uFacex[:,:,1] = uzFacex
        uFacez[:,:,0] = uxFacez
        uFacez[:,:,1] = uzFacez
        
        fluxx = fieldFacex*dot(uFacex, self.mesh.xSf)/self.mesh.cellVolume
        if not self.mesh.xPeriodic:
            fluxx[:,0] *= 0.
        
        fluxz = fieldFacez*dot(uFacez, self.mesh.zSf)/self.mesh.cellVolume
        if not self.mesh.zPeriodic:
            fluxz[-1,:] *= 0.
        
        divField += np.roll(fluxx, -1, axis=1) - fluxx
        divField += np.roll(fluxz,  1, axis=0) - fluxz
        
        return divField
    
    def laplacian(self, field):
        laplacianFieldx = self.mesh.volScalarField.copy()
        laplacianFieldx = (np.roll(field, -1, axis=1) - 2*field + np.roll(field, 1, axis=1))/(2*self.mesh.dx)**2
        if not self.mesh.xPeriodic:
            laplacianFieldx[:,0] = (np.roll(field, -1, axis=1) - field)[:,0]/(2*self.mesh.dx)**2
            laplacianFieldx[:,-1] = (np.roll(field, 1, axis=1) - field)[:,-1]/(2*self.mesh.dx)**2
        
        laplacianFieldz = self.mesh.volScalarField.copy()
        laplacianFieldz = (np.roll(field, -1, axis=0) - 2*field + np.roll(field, 1, axis=0))/(2*self.mesh.dz)**2
        if not self.mesh.zPeriodic:
            laplacianFieldz[0,:] = (np.roll(field, -1, axis=0) - field)[0,:]/(2*self.mesh.dz)**2
            laplacianFieldz[-1,:] = (np.roll(field, 1, axis=0) - field)[-1,:]/(2*self.mesh.dz)**2
        
        return laplacianFieldx + laplacianFieldz
    
    
    def poissonSolver(self, field, solution):
        matrixLength = len(field.flatten())
        matrixToInvert = np.zeros((matrixLength, matrixLength))
        
        lengthX = len(field[0])
        lengthZ = len(field)
        for k in xrange(lengthZ):
            for i in xrange(lengthX):
                index = k*lengthX + i
                matrixToInvert[index][index] -= 4.
                matrixToInvert[index][index-1] += 1.
                matrixToInvert[index][(index+1)%matrixLength] += 1.
                matrixToInvert[index][index-lengthX] += 1.
                matrixToInvert[index][(index+lengthX)%matrixLength] += 1.
        
        if not self.mesh.xPeriodic:
            for k in xrange(lengthZ):
                i = 0
                index = k*lengthX + i
                matrixToInvert[index][index] += 1.
                matrixToInvert[index][index-1] -= 1.
                
                i = lengthX-1
                index = k*lengthX + i
                matrixToInvert[index][index] += 1.
                matrixToInvert[index][(index+1)%matrixLength] -= 1.
        
        if not self.mesh.zPeriodic:
            for i in xrange(lengthX):
                k = 0
                index = k*lengthX + i
                matrixToInvert[index][index] += 1.
                matrixToInvert[index][index-lengthX] -= 1.
                
                k = lengthZ-1
                index = k*lengthX + i
                matrixToInvert[index][index] += 1.
                matrixToInvert[index][(index+lengthX)%matrixLength] -= 1.
                
        # print matrixToInvert
        matrixToInvert *= 1./self.mesh.dx**2
        
        matrixInverted = np.linalg.inv(matrixToInvert)
        
        fieldNew = np.dot(matrixInverted, solution.flatten())
        
        fieldNew2D = np.reshape(fieldNew, (-1, lengthX))
        
        return fieldNew2D