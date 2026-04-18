import pytest
import milmapcon as mmc


@pytest.mark.parametrize(
    'label,zone,grid,x0_test,y0_test',
    [
        ('valid_origin','nord_de_guerre','vS',200000,200000),
        ('invalid_origin','nord_de_guerre','aB',None,None)
    ]
)
def test_get_origin(label, zone,grid, x0_test, y0_test):

    '''Test that get_origin returns a valid x0, y0 for a good origin and None otherwise'''

    x0, y0 = mmc.get_origin(zone, grid)

    assert (x0, y0) == (x0_test, y0_test), f'x0 or y0 value incorrect for {label} test'