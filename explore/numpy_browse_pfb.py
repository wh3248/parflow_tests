#########################
# BrowsePfb
#
# Utility to browse a parflow *.pfb file
#########################
import sys
import os
import logging
import xarray as xr
import numpy as np
import time
rootdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(rootdir)

from pf_xarray.pf_backend import ParflowBackendEntrypoint
from pf_xarray.io import ParflowBinaryReader

class BrowsePfb:
    def __init__(self):
        self.pfb_file_name = None
        self.subgrid_number = 0

    def run(self):
        try:
            self.read_args()
            if not os.path.exists(self.pfb_file_name):
                print(f"File '{self.pfb_file_name}' does not exist.")
                sys.exit(-1)
            # Read the pfb file using PFData and time the load
            start = time.time()
            data = self.read_data()
            duration = time.time() - start

            print("{:.4f} seconds to load using ParflowBinaryReader".format(duration))
            print()

            print(data.shape)
            print(np.sum(data))
        except Exception as e:
            logging.error(str(e))
            sys.exit(-1)

    def read_data(self):
        with ParflowBinaryReader(self.pfb_file_name) as pfb:
            start = time.time()
            data = pfb.read_all_subgrids()
            duration = time.time() - start

            print("{:.4f} seconds to read all subgrids using ParflowBinaryReader".format(duration))
            return data

    def read_args(self):
        if len(sys.argv) < 2:
            print("Error: PFB file name is required.")
            sys.exit(-1)            
        self.pfb_file_name = sys.argv[1]
        if len(sys.argv) > 2:
            self.num_sub_grids = int(sys.argv[2])


main = BrowsePfb()
main.run()

