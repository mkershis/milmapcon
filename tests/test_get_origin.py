import milmapcon as mmc

def test_get_origin(known_origin):
    '''Test the get_origin function against a known origin in database'''
    zone = known_origin['zone']
    grid = known_origin['grid']
    x0 = known_origin['x0']
    y0 = known_origin['y0']

    assert zone == 'nord_de_guerre'
    assert grid == 'vS'
    assert x0 == 200000
    assert y0 == 200000