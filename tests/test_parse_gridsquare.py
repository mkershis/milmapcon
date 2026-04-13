import milmapcon as mmc 

def test_parse_gridsquare_4digit(parse_valid_4digit_grid):
    '''Tests that a 4-digit grid square is parsed to the right precision'''

    grid_letters, clean_grid, x_m, x_y = mmc.parse_gridsquare(parse_valid_4digit_grid)
    assert grid_letters == "vS"
    assert clean_grid == "vS0144"
    assert x_m == 1000
    assert x_y == 44000

def test_parse_gridsquare_6digit(parse_valid_6digit_grid):
    '''Tests that a 6-digit grid square is parsed to the right precision'''

    grid_letters, clean_grid, x_m, x_y = mmc.parse_gridsquare(parse_valid_6digit_grid)
    assert grid_letters == "vS"
    assert clean_grid == "vS014448"
    assert x_m == 1400
    assert x_y == 44800

def test_parse_invalid_grid(parse_invalid_grid_numbers):
    '''Tests that an invalid numeric reference yields none for x_m and x_y'''

    _, _, x_m, x_y = mmc.parse_gridsquare(parse_invalid_grid_numbers)
    assert x_m is None 
    assert x_y is None