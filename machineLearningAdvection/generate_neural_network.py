import sys,os
import matplotlib.pyplot as plt

folderMain = os.path.dirname(os.path.realpath(__file__))
folderSrc = os.path.join(folderMain, "src")
execfile( os.path.join(folderSrc, "neuralNetwork.py" ) )
execfile( os.path.join(folderSrc, "plots.py" ) )
execfile( os.path.join(folderSrc, "functions.py" ) )

'''
Code which generates and trains a neural network on
how to advect (move) functions/fields.
The neural network is saved once training has concluded.
'''


filename = "neural_network.dat"
###############################
# Create training data
###############################
n_training_data = 20000             #Number of randomly generated training data sets
n_modes = 1                         #More modes (int) means more complexity
    
print "Generating {} sets of training data".format(n_training_data)
training_data = create_data_set(n_training_data, n_modes)
    

    
###############################
# Create neural network
###############################
print "Creating neural network"
input_data_length = 42
output_data_length = 40

#One intermediate layer
# advect = Network([input_data_length,42,output_data_length])    

#Two intermediate layers
# advect = Network([input_data_length,42,42,output_data_length])    

#Three intermediate layers
# advect = Network([input_data_length,42,42,42,output_data_length])    
# advect = Network([input_data_length,80,80,80,output_data_length])

#Four intermediate layers
# advect = Network([input_data_length,42,42,42,42,output_data_length])    
advect = Network([input_data_length,80,80,80,80,output_data_length])



    
###########################################################
# Get neural network to learn and calibrate weights/biases
###########################################################
deta = 0.1
batch_size = 20
n_epochs = n_training_data/batch_size

print "Training neural network"
advect.SGD(training_data, n_epochs, batch_size, deta)



###########################################################
# Save neural network to file
###########################################################
print "Saving neural network to file {}".format(filename)
neural_network_filename = os.path.join(folderMain, filename)
advect.save(neural_network_filename)


