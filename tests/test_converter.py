import pytest
import milmapcon as mmc

@pytest.mark.parametrize('zone,grid_square,lat_test,lon_test', [
    ('british_cassini', 'wL350780', 52.21665, -0.68511),
    ('irish_cassini', 'iN250800', 53.76897, -7.62082),
    ('french_lambert_1', 'vY876231', 47.87326, -0.5018),
    ('french_lambert_2', 'wM440896', 47.60454, 2.92237),
    ('french_lambert_3', 'bO213190', 44.23749, 5.10817),
    ('italy_north', 'wQ470320', 43.4327, 10.87377),
    ('italy_south', 'wH510230', 37.00124, 14.57304),
    ('nord_de_guerre', 'wX670439', 48.07308, 9.97967),
    ('north_euro_3', 'rM110670', 57.61976, 15.15452)
],ids=lambda v: str(v))
def test_six_digit_precision(zone, grid_square, lat_test, lon_test):

    lat, lon = mmc.Converter(zone).convert(grid_square)

    lat_delta = abs(lat_test - lat)
    lon_delta = abs(lon_test - lon)

    assert lat_delta <= 0.005, f'Latitude delta for {zone} -> {grid_square} = {lat_delta}'
    assert lon_delta <= 0.005, f'Longitude delta for {zone} -> {grid_square} = {lon_delta}'

@pytest.mark.parametrize('zone,grid_square,lat_test,lon_test',[
    ('british_cassini', 'wL4586', 52.28782, -0.53772),
    ('irish_cassini', 'iN1589', 53.85022, -7.77205),
    ('french_lambert_1', 'vY4396', 48.51139, -1.14214),
    ('french_lambert_2', 'wM5921', 46.98631, 3.11284),
    ('french_lambert_3', 'bO2975', 44.73882, 5.22913),
    ('italy_north', 'wQ7914', 43.28133, 11.27644),
    ('italy_south', 'wH3691', 37.61487, 14.40796),
    ('nord_de_guerre', 'wX7319', 47.84753, 10.04993),
    ('north_euro_3', 'rM2984', 57.7834, 15.43626)
],ids=lambda v: str(v))
def test_four_digit_precision(zone, grid_square, lat_test, lon_test):

    lat, lon = mmc.Converter(zone).convert(grid_square)

    lat_delta = abs(lat_test - lat)
    lon_delta = abs(lon_test - lon)

    assert lat_delta <= 0.005, f'Latitude delta for {zone} -> {grid_square} = {lat_delta}'
    assert lon_delta <= 0.005, f'Longitude delta for {zone} -> {grid_square} = {lon_delta}'