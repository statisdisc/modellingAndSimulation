import numpy as np

class wire:
    mu_0 = 4 * np.pi * 10**(-7)
    I = 1
    scale = 10**(-6)
    
    #Initialising function.
    def __init__(self, start, end, size=1):
        self.start = np.array(start)*size
        self.start = np.insert(self.start,2,0.0)
        self.end = np.array(end)*size
        self.end = np.insert(self.end,2,0.0)
        
    #Return magnitude of B-field due to wire from point coord.
    def B(self, coord, mu_0=mu_0, I=I, scale=scale, B_vec=False):
        coord = np.array(coord)
    
        #Find angle theta to start of wire and angle phi to end of wire.
        vec_to_start = coord - self.start
        mod_vec_to_start = np.sqrt(np.dot(vec_to_start,vec_to_start))
        
        vec_to_end = coord - self.end
        mod_vec_to_end = np.sqrt(np.dot(vec_to_end,vec_to_end))
        
        vec_wire = self.end - self.start
        mod_vec_wire = np.sqrt(np.dot(vec_wire,vec_wire))
        
        cos_theta = np.dot(vec_to_start,vec_wire)/float(mod_vec_to_start*mod_vec_wire)
        cos_phi = np.dot(vec_to_end,-vec_wire)/float(mod_vec_to_end*mod_vec_wire)
        
        #Find perpendicular distance to wire.
        g = np.dot(vec_to_start,vec_wire)/float(np.dot(mod_vec_wire,mod_vec_wire))
        d = self.start + g * vec_wire
        vec_to_wire = coord - d
        R = scale * np.sqrt(np.dot(vec_to_wire,vec_to_wire))
        B = (cos_theta + cos_phi) * mu_0 * I / (4 * np.pi * R)
        B *= 1000         #T ---> mT
        
        #Assign variables for B_vec.
        if B_vec == True:
            self.vec_to_wire = np.copy(vec_to_wire)
            self.a = vec_wire/float(mod_vec_wire)
            self.b = np.copy(vec_to_wire)
            self.b[2] = 0
            normalise = float(np.sqrt(np.dot(self.b,self.b)))
            if normalise != 0.:
                self.b = self.b/normalise
            else:
                self.b = np.array([0.,0.,0.])
        
        return B
        
    #Return B-field vector due to wire at coord.
    def B_vec(self, coord):
        B_vector = np.zeros(3)
        
        B = self.B(coord, B_vec=True)

        k_vec = np.zeros(3)
        k_vec[2] = self.a[0]*self.b[1] - self.a[1]*self.b[0]
        
        theta = np.arccos(self.vec_to_wire[2]/float(np.sqrt(np.dot(self.vec_to_wire,self.vec_to_wire))))
        B_vector[2] = k_vec[2]*B*np.sin(theta)
        
        B_xy_plane = abs(B*np.cos(theta))
        theta = np.arccos(abs(self.a[1])/float(np.dot(self.a,self.a)))
        B_vector[0] = np.sign(self.a[1]) * B_xy_plane * np.cos(theta)
        B_vector[1] = -np.sign(self.a[0]) * B_xy_plane * np.sin(theta)
        
        return B_vector
        
    #Do 2 wires intersect?
    def intersect(self, wire_b):
        a = self.start
        b = self.end
        c = wire_b.start
        d = wire_b.end
        
        g = (b[0]-a[0])*(c[1]-a[1]) - (c[0]-a[0])*(b[1]-a[1])
        h = (d[0]-c[0])*(b[1]-a[1]) - (b[0]-a[0])*(d[1]-c[1])
        
        #If parallel, wires do not intersect.
        if h == 0 or h == 0.:
            return False
        
        f = g/float(h)
        
        #x-coord for intersection point.
        x = c[0] + f*(d[0]-c[0])
        
        #Is intersection point in range of wire?
        if d[0] > c[0] and b[0] > a[0]:
            if x > c[0] and x < d[0] and x > a[0] and x < b[0]:
                return True
            else:
                return False
        elif d[0] < c[0] and b[0] < a[0]:
            if x > d[0] and x < c[0] and x > b[0] and x < a[0]:
                return True
            else:
                return False
        elif d[0] > c[0] and b[0] < a[0]:
            if x > c[0] and x < d[0] and x < a[0] and x > b[0]:
                return True
            else:
                return False
        elif d[0] < c[0] and b[0] > a[0]:
            if x > d[0] and x < c[0] and x < b[0] and x > a[0]:
                return True
            else:
                return False
        else:
            #y-coord for intersection point.
            y = c[1] + f*(d[1]-c[1])
            
            if d[1] > c[1] and b[1] > a[1]:
                if y > c[1] and y < d[1] and y > a[1] and y < b[1]:
                    return True
                else:
                    return False
            elif d[1] < c[1] and b[1] < a[1]:
                if y > d[1] and y < c[1] and y > b[1] and y < a[1]:
                    return True
                else:
                    return False
            elif d[1] < c[1] and b[1] > a[1]:
                if y < c[1] and y > d[1] and y > a[1] and y < b[1]:
                    return True
                else:
                    return False
            elif d[1] > c[1] and b[1] < a[1]:
                if y < d[1] and y > c[1] and y > b[1] and y < a[1]:
                    return True
                else:
                    return False
                    
        print "Intersection process failed, wire is a point?"
        return None
        
    #Find angle between two wires.
    def angle(self, wire_b):
        a = self.start - self.end
        b = -(wire_b.end - wire_b.start)
        mod_a = np.sqrt(np.dot(a,a))
        mod_b = np.sqrt(np.dot(b,b))
        
        cos_theta = np.dot(a,b)/float(mod_a*mod_b)
        theta = np.arccos(cos_theta)
        
        return theta