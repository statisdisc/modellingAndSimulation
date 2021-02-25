def dot(field1, field2):
        return field1[:,:,0]*field2[:,:,0] + field1[:,:,1]*field2[:,:,1]
        
def mag(field):
    return np.sqrt( self.dot(field, field) )