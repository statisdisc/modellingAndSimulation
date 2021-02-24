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
        
        #Indeces for longest line on surface
        self.longestEdge = self.longestEdgeIndeces()
        print "Longest edge from vertex {} ({}) to vertex {} ({})".format(self.longestEdge[0], self.vertices[self.longestEdge[0]], self.longestEdge[1], self.vertices[self.longestEdge[1]])
        
        #Leftover index which is not on longest line
        self.vertexShortIndex = [x for x in range(3) if x not in self.longestEdge][0]
        self.vertexShort = self.vertices[self.vertexShortIndex]
        print "Vertex not on longest edge: {} ({})".format(self.vertexShortIndex, self.vertexShort)
        
        #Determine leftover vertex position relative to longest line.
        #0 or 1 for right-angle triangles
        self.vertexShortTranslationFactor = self.translationFactor(self.vertexShort);
        print "Vertex translation factor for vertex {}: {}".format(self.vertexShortIndex, self.vertexShortTranslationFactor)
        
        self.vertexShortNormalIntersection = self.vertices[self.longestEdge[0]] + self.vertexShortTranslationFactor*(self.vertices[self.longestEdge[1]]-self.vertices[self.longestEdge[0]]);
        self.vertexShortNormalVector = self.vertexShort - self.vertexShortNormalIntersection;
    
    #Return indeces of vertices which form the longest line between them
    def longestEdgeIndeces(self):
        edgeVectors = self.vertices - np.roll(self.vertices, -1, axis=0)
        edgeLengths = np.array([np.dot(edgeVectors[0], edgeVectors[0]), np.dot(edgeVectors[1], edgeVectors[1]), np.dot(edgeVectors[2], edgeVectors[2])])
        argMax = np.argmax(edgeLengths)
        
        return [argMax, (argMax+1)%3]
    
    def translationFactor(self, coord):
        x = self.vertices[self.longestEdge[0]]
        y = self.vertices[self.longestEdge[1]]
        z = coord
        
        solution = np.dot(y-x, z-x)/np.dot(y-x, y-x)
        
        return solution
    
    def getNormalVector(self, vectorStart, vectorFinish, coord):
        x = vectorStart
        y = vectorFinish
        z = coord
        
        translationFactor = np.dot(y-x, z-x)/np.dot(y-x, y-x)
        
        coordIntersect = x + translationFactor*(y-x)
        
        return coord - coordIntersect
    
    def intersectPlane(self, vectorOrigin, vectorDirection, reflectivity):
        intersectionPoint = self.intersectionPoint(vectorOrigin, vectorDirection)
        if (type(intersectionPoint) != bool):
            if (self.intersect(intersectionPoint)):
                #Calculate new direction once reflected
                translationFactor = np.dot(vectorOrigin-2*intersectionPoint, self.normalVector)/np.dot(self.normalVector, self.normalVector)
                # vectorDirectionNew = intersectionPoint - vectorOrigin + translationFactor*self.normalVector
                vectorDirectionNew = vectorDirection + 2*self.normalVector*np.sign(np.dot(-self.normalVector, vectorDirection))
                # print "\n", vectorDirection, self.normalVector, vectorDirectionNew
                return intersectionPoint, vectorDirectionNew, reflectivity*self.reflectivity
            else:
                return vectorOrigin, vectorDirection, reflectivity
        else:
            return vectorOrigin, vectorDirection, reflectivity
        
    def intersectionPoint(self, vectorOrigin, vectorDirection):
        if np.dot(vectorDirection, self.normalVector) == 0.:
            return False

        translationFactor = np.dot(self.vertices[0]-vectorOrigin, self.normalVector)/np.dot(vectorDirection, self.normalVector)
        return vectorOrigin + translationFactor*vectorDirection
    
    def intersect(self, intersectionPoint):
        translationFactor = self.translationFactor(intersectionPoint)
        normalVector = intersectionPoint - self.vertexShortNormalIntersection
        
        vec0 = self.getNormalVector(self.vertices[1], self.vertices[2], self.vertices[0])
        vec1 = self.getNormalVector(self.vertices[0], self.vertices[2], self.vertices[1])
        vec2 = self.getNormalVector(self.vertices[1], self.vertices[0], self.vertices[2])
        
        vecIntersectionPoint0 = self.getNormalVector(self.vertices[1], self.vertices[2], intersectionPoint)
        vecIntersectionPoint1 = self.getNormalVector(self.vertices[0], self.vertices[2], intersectionPoint)
        vecIntersectionPoint2 = self.getNormalVector(self.vertices[1], self.vertices[0], intersectionPoint)
        
        if (np.dot(vec0, vecIntersectionPoint0) >= 0) and (np.dot(vec1, vecIntersectionPoint1) >= 0) and (np.dot(vec2, vecIntersectionPoint2) >= 0):
            return True
        else:
            return False