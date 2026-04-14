import pytest
import milmapcon as mmc 

@pytest.mark.parametrize(
    'label,zone,grid,x,y,E_test,N_test',
    [
        ('good_grid_input','nord_de_guerre','vS',1400,44800,201400,244800),
        ('bad_grid_and_xy','nord_de_guerre','aB',None,None,None,None),
        ('bad_numbers','nord_de_guerre','vS',None,None,None,None),
        ('bad_grid_only','nord_de_guerre','aB',1400,44800,None,None)

    ]
)
def test_en_from_grid(label, zone, grid, x, y, E_test, N_test):
    '''Test EN from grid with varying inputs'''

    E, N = mmc.EN_from_grid(zone, grid, x, y)

    assert E == E_test, f'Easting for {label} test is incorrect'
    assert N == N_test, f'Northing for {label} test is incorrect'