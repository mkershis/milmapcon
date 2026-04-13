import milmapcon as mmc 

def test_good_input(en_grid_good_input):
    '''Test good input'''
    zone = en_grid_good_input['zone']
    grid = en_grid_good_input['grid']
    x = en_grid_good_input['x']
    y = en_grid_good_input['y']

    E, N = mmc.EN_from_grid(zone, grid, x, y)

    assert E is not None, 'E should not be None'
    assert N is not None, 'E should not be None'

def test_bad_grid_and_nums(en_grid_bad_grid_and_xy):
    '''Test bad grid ref and numbers'''
    zone = en_grid_bad_grid_and_xy['zone']
    grid = en_grid_bad_grid_and_xy['grid']
    x = en_grid_bad_grid_and_xy['x']
    y = en_grid_bad_grid_and_xy['y']
    
    E, N = mmc.EN_from_grid(zone, grid, x, y)

    assert E is None, 'E should be None'
    assert N is None, 'N should be None'

def test_bad_grid_nums(en_grid_bad_nums):
    '''Test good zone but bad numbers'''
    zone = en_grid_bad_nums['zone']
    grid = en_grid_bad_nums['grid']
    x = en_grid_bad_nums['x']
    y = en_grid_bad_nums['y']

    E, N = mmc.EN_from_grid(zone, grid, x, y)
    
    assert E is None, 'E should be None'
    assert N is None, 'N should be None'

def test_bad_grid(en_grid_bad_grid):
    '''Tests a bad grid'''
    zone = en_grid_bad_grid['zone']
    grid = en_grid_bad_grid['grid']
    x = en_grid_bad_grid['x']
    y = en_grid_bad_grid['y']

    E, N = mmc.EN_from_grid(zone, grid, x, y)

    assert E is None, 'E should be None'
    assert N is None, 'N should be None'