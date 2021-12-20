import sys
import os
import unittest


import xarray as xr
rootdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(rootdir)

from pf_xarray.pf_backend import ParflowBackendEntrypoint
from pf_xarray.io import ParflowBinaryReader

class TestPFData(unittest.TestCase):

    def test_open_dataset(self):
        """Test reading a pfb file using xarray open_dataset."""

        pfb_file_name = './data/default_single.out.press.00000.pfb'
        ds = xr.open_dataset(pfb_file_name, name='xxdefault_single', engine=ParflowBackendEntrypoint)

        # Check the sizes of the dimensions from the loaded xarray
        self.assertEqual(3, len(ds.dims))
        self.assertEqual(0, len(ds.coords))
        self.assertEqual(8, ds.dims["z"])
        self.assertEqual(18, ds.dims["x"])
        self.assertEqual(15, ds.dims["y"])

        # Check that we can read a cell from the data grid
        da = ds.to_array()
        self.assertEqual(13, int(float(da[0][0][0][0])))

    def test_headers_in_read_all_subgrids(self):
        """Test reading a pfb file using ParflowBinaryReader class and check pfb headers."""

        pfb_file_name = './data/default_single.out.press.00000.pfb'
        with ParflowBinaryReader(pfb_file_name) as pfb:
            data = pfb.read_all_subgrids()
            self.assertEqual(18, int(pfb.header.get('nx')))
            self.assertEqual(15, int(pfb.header.get('ny')))
            self.assertEqual(8, int(pfb.header.get('nz')))
            self.assertEqual(8, int(pfb.header.get('dx')))
            self.assertEqual(10, int(pfb.header.get('dy')))
            self.assertEqual(1, int(pfb.header.get('dz')))
            self.assertEqual(-10, int(pfb.header.get('x')))
            self.assertEqual(10, int(pfb.header.get('y')))
            self.assertEqual(1, int(pfb.header.get('z')))
            self.assertEqual(1, int(pfb.header.get('p')))
            self.assertEqual(1, int(pfb.header.get('q')))
            self.assertEqual(1, int(pfb.header.get('r')))
            self.assertEqual(1, int(pfb.header.get('n_subgrids')))

    def test_read_pfsb(self):
        """Test reading a pfb file using ParflowBinaryReader class and check pfb headers."""

        return
        pfb_file_name = './data/default_single.out.concen.0.00.00000.pfsb'
        with ParflowBinaryReader(pfb_file_name) as pfb:
            data = pfb.read_all_subgrids()

if __name__ == '__main__':
        unittest.main()