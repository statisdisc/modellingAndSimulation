import os
import sys

class folders:
    def __init__(self, folderScripts="", folderData=""):
        # Folder containing scripts to execute
        if folderScripts == "":
            folderScripts = sys.path[0]
        self.scripts = folderScripts
        
        # Root directory, typically parent directory to scripts folder
        self.root = os.path.dirname(self.scripts)
        
        # Folder containing source code
        self.src = os.path.join(self.root, "src")
        
        # Folder containing data to be analysed
        if folderData == "":
            folderData = os.path.join(self.root, "data")
        self.data = folderData
        
        # Folder for output files and images
        self.outputs = os.path.join(self.root, "outputs")
        
        if not os.path.isdir(self.outputs):
            os.makedirs(self.outputs)