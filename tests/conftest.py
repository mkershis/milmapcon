import pytest

# fixtures for the test_parse_gridquare.py tests
@pytest.fixture
def parse_valid_4digit_grid():
    return "vS0144"

@pytest.fixture
def parse_valid_6digit_grid():
    return "vS014448"

@pytest.fixture
def parse_invalid_grid_numbers():
    return "vS014"

# fixtures for the test_get_origin.py tests

@pytest.fixture
def known_origin():
    return {
        'zone':'nord_de_guerre',
        'grid':'vS',
        'x0':200000,
        'y0':200000
    }

# fixtures for the test_get_crs
@pytest.fixture 
def known_crs_string():
    return '+proj=lcca +lat_0=49.5 +lon_0=7.737208333 +x_0=600000 +y_0=300000 +a=6376523 +rf=308.64 +k_0=0.9996256'