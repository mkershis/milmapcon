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