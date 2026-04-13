import milmapcon as mmc

def test_get_origin(known_origin):
    '''Test the get_origin function against a known origin in database'''

    x0, y0 = mmc.get_origin(known_origin['zone'], known_origin['grid'])

    assert x0 == known_origin['x0'], 'x0 value is not correct'
    assert y0 == known_origin['y0'], 'y) value is not correct'

def test_get_origin_invalid(invalid_origin):
    '''Test that get_origin return None on an invalid grid reference'''

    x0, y0 = mmc.get_origin(invalid_origin['zone'], invalid_origin['grid'])

    assert x0 is None, 'x0 value should be None'
    assert y0 is None, 'y0 value should be None'