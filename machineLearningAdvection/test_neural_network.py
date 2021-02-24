import sys,os
import matplotlib.pyplot as plt

folderMain = os.path.dirname(os.path.realpath(__file__))
folderSrc = os.path.join(folderMain, "src")
execfile( os.path.join(folderSrc, "neuralNetwork.py" ) )
execfile( os.path.join(folderSrc, "plots.py" ) )
execfile( os.path.join(folderSrc, "functions.py" ) )

'''
generate_neural_network.py must be run at least once.
This code reads the neural network output by
generate_neural_network.py and runs it for some randomised
test cases and outputs the plots of how it performs.
Requires imagemagick on Windows to make a gif.
'''

gif = True
###########################################################
# Load neural network from file
###########################################################
print "Loading neural network"
directory = folderMain
# directory = os.path.join(folderMain, "some_other_folder")
neural_network_filename = os.path.join(directory , "neural_network.dat")

if not os.path.isfile(neural_network_filename):
    neural_network_filename = os.path.join(directory, "neural_network_20000testData.dat")
advect = load(neural_network_filename)



###########################################################
# Generate data sets to test
###########################################################
print "Generating test simulations"
n_modes = 1
test_data = create_data_set(3, n_modes)
test_data.append( create_data_set(1, 2)[0] )
test_data.append( create_data_set(1, 1, square=True)[0] )



###########################################################
# Plot all advection test simulations
###########################################################
#Black = analytic solution
#Blue = existing method (FTBS)
#Red = neural network output
image_files = plot_all_simulations(test_data)



###########################################################
# Generate animations
###########################################################
print "Creating gifs and deleting image files"
if gif == True:
    print 50*"="
    print "\n\nWARNING: You have chosen to generate a gif animation. You must have imagemagick installed or this will not work.\n\n"
    print 50*"="
    
    for i in xrange(len(image_files)):
        gif_file = os.path.join(folderMain, "gif_{}.gif".format(i) )
        make_gif(gif_file, image_files[i], delay=100)
        
        # delete_files(image_files[i][1:len(image_files[i])-1])   