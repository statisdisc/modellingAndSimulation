import numpy as np

class surface:
    def __init__(self, vertices=[[0.,0.,0.], [1.,0.,0.], [0.,1.,0.]], reflectivity=1.):
        if (type(vertices) != list):
            raise ValueError("vertices must be of type list")
        
        if (len(vertices) != 3):
            raise ValueError("Surface must have exactly 3 vertices")
        
        if (len(vertices[0]) != 3) or (len(vertices[1]) != 3) or (len(vertices[2]) != 3):
            raise ValueError("Vertices must be a 3D vector (length 3)")
        
        self.vertices = np.array(vertices)
        self.reflectivity = reflectivity
        
        self.normalVector = np.cross(self.vertices[1]-self.vertices[0], self.vertices[2]-self.vertices[0])
        self.normalVector *= 1./np.dot(self.normalVector, self.normalVector)
        
        #Indices for longest line on surface
        self.longestEdge = self.longestEdgeIndeces()
        print("Longest edge from vertex {} ({}) to vertex {} ({})".format(self.longestEdge[0], self.vertices[self.longestEdge[0]], self.longestEdge[1], self.vertices[self.longestEdge[1]]))
        
        #Leftover index which is not on longest line
        self.vertexShortIndex = [x for x in range(3) if x not in self.longestEdge][0]
        self.vertexShort = self.vertices[self.vertexShortIndex]
        print("Vertex not on longest edge: {} ({})".format(self.vertexShortIndex, self.vertexShort))
        
        #Determine leftover vertex position relative to longest line.
        #0 or 1 for right-angle triangles
        self.vertexShortTranslationFactor = self.translationFactor(self.vertexShort);
        print("Vertex translation factor for vertex {}: {}".format(self.vertexShortIndex, self.vertexShortTranslationFactor))
        
        self.vertexShortNormalIntersection = self.vertices[self.longestEdge[0]] + self.vertexShortTranslationFactor*(self.vertices[self.longestEdge[1]]-self.vertices[self.longestEdge[0]]);
        self.vertexShortNormalVector = self.vertexShort - self.vertexShortNormalIntersection;
    
    def dot(self, vector1, vector2):
        "Dot product for the inner-most array elements"
        return np.sum(vector1*vector2, axis=-1)
    
    def mag(self, vector):
        return np.sqrt(self.dot(vector, vector))
    
    #Return indices of vertices which form the longest line between them
    def longestEdgeIndeces(self):
        edgeVectors = self.vertices - np.roll(self.vertices, -1, axis=0)
        edgeLengths = np.array([self.dot(edgeVectors[0], edgeVectors[0]), self.dot(edgeVectors[1], edgeVectors[1]), self.dot(edgeVectors[2], edgeVectors[2])])
        argMax = np.argmax(edgeLengths)
        
        return [argMax, (argMax+1)%3]
    
    def translationFactor(self, coord):
        x = self.vertices[self.longestEdge[0]]
        y = self.vertices[self.longestEdge[1]]
        z = coord
        
        solution = self.dot(y-x, z-x)/self.dot(y-x, y-x)
        
        return solution
    
    def getNormalVector(self, vectorStart, vectorFinish, coord):
        x = vectorStart
        y = vectorFinish
        z = coord
        
        translationFactor = self.dot(y-x, z-x)/self.dot(y-x, y-x)
        
        if type(translationFactor) != np.ndarray:
            coordIntersect = x + translationFactor*(y-x)
        else:
            coordIntersect = x + translationFactor[:,None]*(y-x)[None,:]
        
        return coord - coordIntersect
    
    def intersectSurface(self, vectorOrigin, vectorDirection, intensity):
        '''
        Determine whether an incident vector intersects this surface.
        vectorOrigin and vectorDirection must be of the 2D form:
        [[a1,a2,a3],[b1,b2,b3],[b1,b2,b3],...,[h1,h2,h3]]
        '''
        if vectorOrigin.ndim == 1:
            raise ValueError("Input vectors must be 2D")
        
        indices = np.arange(len(vectorOrigin))
        
        intersectionPoints, conditionIntersect = self.intersect(vectorOrigin, vectorDirection)
        indices = indices[conditionIntersect]
        intersectionPoints = intersectionPoints[conditionIntersect]
        
        if len(indices) > 0:
            #Calculate new direction once reflected
            translationFactor = self.dot(vectorOrigin[conditionIntersect]-2*intersectionPoints, self.normalVector)/self.mag(self.normalVector)
            vectorDirectionNew = vectorDirection[conditionIntersect] + 2*self.normalVector[None,:]*np.sign(self.dot(-self.normalVector, vectorDirection[conditionIntersect]))[:,None]
            
            vectorOrigin[indices] = intersectionPoints
            vectorDirection[indices] = vectorDirectionNew
            intensity[indices] *= self.reflectivity
        
        return vectorOrigin, vectorDirection, intensity
        
    def intersectionPointOnPlane(self, vectorOrigin, vectorDirection):
        '''
        This surface is defined on a 2D plane. For a given vector, see where the intersection point
        is with the plane.
        This can be used to determine whether the intersection point is on the actual surface.
        '''
        # Remove points which are parallel to the plane and won't intrsect
        conditionParallel = self.dot(vectorDirection, self.normalVector) == 0.
        vectorOrigin[conditionParallel] *= np.nan
        vectorDirection[conditionParallel] *= np.nan
        
        translationFactor = self.dot(self.vertices[0]-vectorOrigin, self.normalVector)/self.dot(vectorDirection, self.normalVector)
        return vectorOrigin + translationFactor[...,None]*vectorDirection, np.invert(conditionParallel)
    
    def intersect(self, vectorOrigin, vectorDirection):
        intersectionPoints, condition0 = self.intersectionPointOnPlane(vectorOrigin, vectorDirection)
        
        translationFactor = self.translationFactor(intersectionPoints)
        normalVector = intersectionPoints - self.vertexShortNormalIntersection
        
        vec0 = self.getNormalVector(self.vertices[1], self.vertices[2], self.vertices[0])
        vec1 = self.getNormalVector(self.vertices[0], self.vertices[2], self.vertices[1])
        vec2 = self.getNormalVector(self.vertices[1], self.vertices[0], self.vertices[2])
        
        vecIntersectionPoint0 = self.getNormalVector(self.vertices[1], self.vertices[2], intersectionPoints)
        vecIntersectionPoint1 = self.getNormalVector(self.vertices[0], self.vertices[2], intersectionPoints)
        vecIntersectionPoint2 = self.getNormalVector(self.vertices[1], self.vertices[0], intersectionPoints)
        
        condition1 = self.dot(vecIntersectionPoint0, vec0) >= 0
        condition2 = self.dot(vecIntersectionPoint1, vec1) >= 0
        condition3 = self.dot(vecIntersectionPoint2, vec2) >= 0
        
        return intersectionPoints, condition0*condition1*condition2*condition3