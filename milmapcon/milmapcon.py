
import sqlite3
from pathlib import Path
import os
import sys
import webbrowser
from pyproj import CRS, Transformer


# Get the parent directory from where the gridsquare.py file lives. From here we can define the correct
# path to the data files
main_path = Path(__file__).parent
data_dir = Path(main_path, 'gs_data.db') 

def show_zones():
    ''' 
    Utility function to show which zones are currently supported
    by querying the parameters table and printing the zone names
    '''
    with sqlite3.connect(data_dir) as con:
        cur = con.cursor()
        zones = cur.execute('select zone from parameters').fetchall()
    
    print('The following zones are currently supported:')
    print('Please use these exact strings in defining the zone.\n')
    
    for i, zone in enumerate(zones, start=1):
        print(f'\t{i}). "{zone[0]}"')
        
    

def get_origin(zone_name: str, grid_letters: str) -> tuple[int]:
    '''
    Gets the origin (x0, y0) for the specified zone
    and grid square to calculate the actual position in meters.
    If no such grid is found in that zone, None is returned.

    Paramters:
        zone_name (str): Name of the map zone
        grid_letters (str): Two-letter grid reference
    
    Returns:
        x0 (int): Easting for the grid origin in meters
        y0 (int): Northing for the grid origin in meters
    '''
    with sqlite3.connect(data_dir) as con:
        cur = con.cursor()

        # there should only be one x0, y0 pair since the zone-grid combo
        # is designed to be unique in the origins table
        result = cur.execute(f'select x0, y0 from origins where zone="{zone_name}" and grid="{grid_letters}"').fetchone()

        if result:
            x0, y0 = result
        else:
            x0 = y0 = None

    return x0, y0

def parse_gridsquare(grid_square: str) -> tuple[str, str, int, int]:
    ''' 
    Parses grid square and ensures the data is in the correct format.
    Returns "None" values if grid doesn't exist in the selected zone
    or if the numeric reference is invalid

    Parameters:
        grid_square (str): raw input of grid reference

    Returns:
        grid_letters (str): Two-letter grid reference
        clean_grid (str): Clean grid_square reference with proper capitalization and
                            without whitespace or special characters
        x_m (int): Relative Easting derived from the first half of the grid reference
        y_m (int): Relative Northing derived from the second half of the grid reference
    '''

    grid_letters = ''
    grid_numbers = ''

    # trims whitespace regarless of its position in the input
    # enforces proper grid letter capitalization

    for character in str(grid_square):
        if (character.isalpha()) & (len(grid_letters) == 0):
            grid_letters += character.lower()
        elif (character.isalpha()) & (len(grid_letters) == 1):
            grid_letters += character.upper()
        elif character.isdigit():
            grid_numbers += character

    clean_grid = grid_letters + grid_numbers
    x_m = y_m = 0

    # checks the precision of the grid reference to calculate the magnitude
    # correctly

    if len(grid_numbers) == 4:
        x_m += (int(grid_numbers[0:2]) * 1000)
        y_m += (int(grid_numbers[2:]) * 1000)
    elif len(grid_numbers) == 6:
        x_m += (int(grid_numbers[0:3]) * 100)
        y_m += (int(grid_numbers[3:]) * 100)
    else:
        x_m = y_m = None
    
    return grid_letters, clean_grid, x_m, y_m

def gen_crs() -> dict:
    ''' 
    Load CRS string parameters from database and return dictionary of CRS objects

    Returns:
        dictionary of the CRS objects where the key is the map zone and the value
        is the CRS object
    '''
    crs_dict = {}
    with sqlite3.connect(data_dir) as con:
        cur = con.cursor()
        param_list = cur.execute('select * from parameters').fetchall()
    
    for row in param_list:

        label, params = row[0], row[1:]
        param_labels = ['+proj','+lat_0','+lon_0','+x_0','+y_0','+a','+rf','+k_0','+ellps']
        string = ''

        for param_label, param in zip(param_labels, params):
            if param != '':
                string += f'{param_label}={param} '
        crs_dict[label] = string.strip()

        #print(f'"{label}" -- > "{string.strip()}"') # can uncomment to check formatting, etc.

        crs_dict[label] = CRS.from_string(string.strip())
    return crs_dict


def EN_from_grid(zone_name: str, grid: str,x:int,y:int, print_warnings=True) -> tuple[int, int]:
    ''' 
    Calculates the full Easting and Northing given the grid reference and
    relative easting/northing

    Parameters:
        zone_name (str): Name of the map zone
        grid (str): Two-letter designation for the grid
        x (int): Relative Easting to grid origin
        y (int): Relative Northing to grid origin
        print_warnings (bool): True/False to show warnings
    
    Returns:
        E (int): Absolute Easting in meters
        N (int): Absolute Northing in meters
    '''
    
    x0, y0 = get_origin(zone_name, grid)

    if (x == y == None) & (x0 == y0 == None):
        if print_warnings:
            print(f'{clean_grid}: Coordinates are invalid and grid doesn\'t exist in this zone')
        E = N = None
    elif (x == y == None):
        if print_warnings:
            print(f'{clean_grid}: Grid numbers invalid. Must be 4 or 6 digits long')
        E = N = None
    elif (x0 == y0 == None):
        if print_warnings:
            print(f'{clean_grid}: Two letter grid not valid for this zone')
        E = N = None
    else:
        x0, y0 = get_origin(zone_name, grid)
        E = x0 + x
        N = y0 + y
    return E, N

def get_lat_lon(zone_name: str, crs_dict: dict, E: int, N: int) -> tuple[float, float]:
    ''' 
    Function which takes the zone, Easting, and Northing and
    calculates the latitude and longitude. 

    Parameters:
        zone_name (str): Name of the map zone
        crs_dict (dict): Dictionary of CRS objects
        E (int): Easting in meters
        N (int): Northing in meters

    Returns:
        lat (float): Latitude in degrees, decimal format
        lon (float): Longitude in degrees, decimal format
    '''
    if E == N == None:
        lat = lon = None
    else:
        from_crs = crs_dict[zone_name]
        to_crs = CRS.from_epsg(4326)
        trans = Transformer.from_crs(from_crs, to_crs)
        lat, lon = trans.transform(E, N)
    return lat, lon

def grid_search(x0: int,y0: int, zone_name: str) -> str:
    ''' 
    Given the zone and origin, identify the correct grid square
    Return the two-letter grid

    Parameters:
        x0 (int): Easting of the grid's origin
        y0 (int): Northing of the grid's origin
        zone_name (str): Name of the grid

    Return:
        grid (str): Two-letter grid designation
    '''
    with sqlite3.connect(data_dir) as con:
        cur = con.cursor()
        grid = cur.execute(f'select grid from origins where x0 ={x0} and y0={y0} and zone="{zone_name}"').fetchone()

    if grid != None:
        return grid[0]
    else:
        return None

def show_map(lat: float, lon: float):
    ''' 
    Takes lat/lon input and searches Google Maps for
    the coordinates, opening a webbrowser page
    in the process.

    Parameters:
        lat (float): latitude in degrees, decimal format
        lon (float): longitude in degrees, decimal format

    '''

    search_string = f'https://www.google.com/maps/search/?api=1&query={lat},{lon}'
    webbrowser.open(search_string)

class Converter:
    ''' 
    Class representing the gridsquare converter object.

    Attributes:
        zone_name (str): The map zone you are converting from
        from_crs (object): pyproj CRS for the zone you are converting from
        to_crs (object): pyproj CRS for WGS 84
        print_warnings (bool): Boolean flag indicating whether you wish to print warnings/error messages
    '''

    def __init__(self, zone_name: str, print_warnings: bool = True):
        ''' 
        The constructor for the Converter class

        Parameters:
            zone_name (str): The map zone you are converting from
            print_warnings (bool): Boolean flag indicating whether you wish to print warnings/error messages

        '''
        self.zone_name = zone_name
        self.from_crs = _crs_dict[zone_name]
        self.to_crs = CRS.from_epsg(4326)
        self.print_warnings = print_warnings

    def convert(self, grid_input: str) -> tuple[float, float]:
        ''' 
        Main method for converting grid square references to latitude and longitude values

        Parameters:
            grid_input (str): Must be a 6 or 8 character string starting with two letters
            specifying the grid square in the zone of interest followed by either 4 or 6
            numbers. Input is not case sensitive, and any whitespaces or non-alphanumeric characters
            will be cleaned out prior to processing.

        Returns:
            lat (float): latitude
            lon (float): longitude
        '''
        grid, clean_grid_ref, x_m, y_m = parse_gridsquare(grid_input)
        E,N = EN_from_grid(self.zone_name, grid, x_m, y_m, self.print_warnings)
        if (E == N == None) & self.print_warnings:
            print(f'Couldn\'t calculate E,N values. Check to see that "{grid_input}" is a valid grid square for "{self.zone_name}"')
            lat = lon = None
        elif (E == N == None) & (not self.print_warnings):
            lat = lon = None
        else:
            trans = Transformer.from_crs(self.from_crs, self.to_crs)
            lat, lon = trans.transform(E,N)

            # Sometimes if one of the original grid coordinates is zero, you get inf, inf
            # as a result of the transformation. The following conditional checks for this
            # and adds 1 meter to either the Easting or Northing to push the coordinate slightly
            # into an acceptable zone. Tends to occur on grid squares at the perimeter
            # of the zone and, since it's only 1 meter, it should have a negligible impact on accuracy.

            if lat == lon == float('inf'):
                if x_m == 0:
                    lat, lon = trans.transform(E + 1, N)
                elif y_m == 0:
                    lat, lon = trans.transform(E, N + 1)
        return lat, lon

_crs_dict = gen_crs()

def main():
    # main can be used for quick debugging as well as displaying the result
    # in a google map page

    zone = 'nord_de_guerre'
    grid_ref = 'vS015449'

    converter = Converter(zone)
    lat, lon = converter.convert(grid_ref)
    print(f'The lat/lon for "{grid_ref}" in the "{zone}" zone is ({lat},{lon})')
    show_map(lat, lon)
        
if __name__ == '__main__':
    main()