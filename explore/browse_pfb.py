#########################
# BrowsePfb
#
# Utility to browse a parflow *.pfb file
#########################
import sys
import os
import logging
import time
import numpy as np
from parflowio.pyParflowio import PFData

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

            print("{:.4f} seconds to load using PFData".format(duration))
            print()
            self.printPFData(data)
        except Exception as e:
            logging.error(str(e))
            sys.exit(-1)

    def read_data(self):
            pfdata = PFData(self.pfb_file_name)
            pfdata.loadHeader()
            pfdata.loadPQR()

            return pfdata

    def printPFData(self, pfdata):
       num_sub_grids = pfdata.getNumSubgrids()
       x = pfdata.getX()
       y = pfdata.getY()
       z = pfdata.getZ()
       dx = pfdata.getDX()
       dy = pfdata.getDY()
       dz = pfdata.getDZ()
       nx = pfdata.getNX()
       ny = pfdata.getNY()
       nz = pfdata.getNZ()
       p = pfdata.getP()
       q = pfdata.getQ()
       r = pfdata.getR()
       order = pfdata.getIndexOrder()

       print(f"#SubGrids:{num_sub_grids} PQR=({p}, {q}, {r}) XYZ=({x}, {y}, {z}) NXYZ=({nx}, {ny}, {nz}) DXYZ=({dx}, {dy}, {dz})")

       pfdata.loadData()
       data = pfdata.moveDataArray()
       d1 = len(data[0])
       d2 = len(data[0][0])
       print(f"Dimension sizes: ({d1}, {d2})")
       print(data[0][0][0])

    def read_args(self):
        if len(sys.argv) < 2:
            print("Error: PFB file name is required.")
            sys.exit(-1)            
        self.pfb_file_name = sys.argv[1]
        if len(sys.argv) > 2:
            self.num_sub_grids = int(sys.argv[2])


main = BrowsePfb()
main.run()

