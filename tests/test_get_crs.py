import milmapcon as mmc 
from pyproj import CRS

def test_gen_crs(known_crs_string):
    '''Tests that the database connection and string creation works'''

    test_crs = CRS.from_string(known_crs_string) # this is the nord_de_guerre zone

    crs_dict = mmc.gen_crs()

    assert test_crs == crs_dict['nord_de_guerre'], "CRS object generation error"