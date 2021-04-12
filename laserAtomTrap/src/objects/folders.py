import os
import sys

class folders:
    def __init__(self, folderScripts="", folderOutputs=""):
        if folderScripts == "":
            folderScripts = sys.path[0]
        
        # Folder containing all scripts run by the user
        self.scripts = folderScripts
        
        # Folder containing all source code and scripts
        self.root = os.path.dirname(self.scripts)
        
        # Folder containing all source code
        self.src = os.path.join(self.root, "src")
        
        # Folder for the output files and images
        if folderOutputs == "":
            self.outputs = os.path.join(self.root, "outputs")
        else:
            self.outputs = folderOutputs
        
        if not os.path.isdir(self.outputs):
            os.makedirs(self.outputs)