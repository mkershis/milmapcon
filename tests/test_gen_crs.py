import milmapcon as mmc 
from pyproj import CRS

def test_gen_crs():
    '''Tests that the database connection and string creation works'''
    known_crs_string = '+proj=lcca +lat_0=49.5 +lon_0=7.737208333 +x_0=600000 +y_0=300000 +a=6376523 +rf=308.64 +k_0=0.9996256'
    test_crs = CRS.from_string(known_crs_string) # this is the nord_de_guerre zone

    crs_dict = mmc.gen_crs()

    assert test_crs == crs_dict['nord_de_guerre'], "CRS object generation error"