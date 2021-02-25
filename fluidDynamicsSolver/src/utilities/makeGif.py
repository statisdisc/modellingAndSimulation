'''
Create a gif animation given an array of image files.
'''
import os
import sys
import warnings

# Plot the horizontally averaged volume fraction
def makeGif(
        filenameFinal, imageList,
        folder="",
        delay=10,
        subGifLimit=50,
        system="unix"
    ):
    print "\nCreating gif animation: {}".format(filenameFinal)
    
    # Convert command for imagemagick, operating system dependent
    convert = "convert"
    if system == "windows":
        convert = "magick convert"
    
    # Create folder for gif output
    folderGif = os.path.join(folder, "gifs")
    if not os.path.isdir(folderGif):
        os.makedirs(folderGif)
    
    
    # Create temporary smaller gifs due to command line and memory restrictions
    temporaryGifs = []
    for i in xrange((len(imageList)-1)/subGifLimit + 1):
        start = i*subGifLimit
        finish = min((i+1)*subGifLimit, len(imageList))
        
        print "Making temporary gif {} (Images {}-{})".format(i+1, start, finish)
        
        console = "{} -delay {} ".format(convert, delay)
        for j in xrange(start, finish):
            filename = imageList[j]
            
            if os.path.isfile(filename):
                console += "{} ".format(filename)
            else:
                warnings.warn("Image file does not exist and will be excluded: {}".format(filename))
                
        filenameGif = os.path.join(folderGif, "tempGif_{}.gif".format(i+1))
        temporaryGifs.append(filenameGif)
        console += "{} ".format(filenameGif)
        os.system(console)
            
            
    if len(imageList)/subGifLimit > 1:
        print "Stiching all gifs together"
        console = "{} ".format(convert)
        for filename in temporaryGifs:
            console += "{} ".format(filename)
        filenameGif = os.path.join(folderGif, filenameFinal)
        console += "{} ".format(filenameGif)
        os.system(console)
        
        # Delete temporary gifs
        for filename in temporaryGifs:
            print "Deleting {}".format(filename)
            os.remove(filename)
    else:
        console = "mv {} {}".format(filenameGif, os.path.join(folderGif, filenameFinal))
        os.system(console)
    
    