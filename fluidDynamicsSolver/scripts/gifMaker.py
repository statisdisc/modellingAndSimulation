import os,sys
import numpy as np

testcases = []
testcases.append({"filename": "z_kh"})

times = range(0, 10000, 100)

folder_gif = sys.path[0]

for testcase in testcases:
    print testcase["filename"]
    console = "magick convert -delay 10 "
    filename_gif = "{}.gif".format(testcase["filename"])
    
    for time in times:
        
        filename = os.path.join(sys.path[0], "{}_{}.png ".format(testcase["filename"], time))
        # print filename
        console += filename
        
    console += "-loop 0 {}".format( os.path.join(folder_gif, filename_gif) )
    os.system(console)