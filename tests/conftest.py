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