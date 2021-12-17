#########################
# BrowsePfb
#
# Utility to browse a parflow *.pfb file
#########################
import sys
import os
import logging
from parflowio.pyParflowio import PFData

class BrowsePfb:
    def __init__(self):
        self.pfb_file_name = None

    def run(self):
        try:
            self.read_args()
            if not os.path.exists(self.pfb_file_name):
                print(f"File '{self.pfb_file_name}' does not exist.")
                sys.exit(-1)
            pfdata = PFData(self.pfb_file_name)
            pfdata.loadHeader()
            print(pfdata)
        except Exception as e:
            logging.error(str(e))
            sys.exit(-1)

    def read_args(self):
        if len(sys.argv) < 2:
            print("Error: PFB file name is required.")
            sys.exit(-1)            
        self.pfb_file_name = sys.argv[1]

main = BrowsePfb()
main.run()

