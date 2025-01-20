''' 
MIT License

Copyright (c) 2025 Matt Kershis

URL: https://github.com/mkershis/milmapcon

milmapcon is a Python library (built using pyproj) which converts 4 or 6 digit
grid coordinates from WWII-era maps into latitude and longitude coordinates
in the WGS 84 coordinate system.

Classes:
    Converter:
 
        Class representing the milmapcon converter object.

        Attributes:
            zone_name (str): The map zone you are converting from
            from_crs (object): pyproj CRS for the zone you are converting from
            to_crs (object): pyproj CRS for WGS 84
            print_warnings (bool): Boolean flag indicating whether you wish to print warnings/error messages
    
        Methods:

            __init__(self, zone_name: str, print_warnings: bool = True):

                The constructor for the Converter class

                Parameters:
                    zone_name (str): The map zone you are converting from
                    print_warnings (bool): Boolean flag indicating whether you wish to print warnings/error messages

            convert(self, grid_input: str) -> tuple[float, float]:

                Main method for converting grid square references to latitude and longitude values

                Parameters:
                    grid_input (str): Must be a 6 or 8 character string starting with two letters
                    specifying the grid square in the zone of interest followed by either 4 or 6
                    numbers. Input is not case sensitive, and any whitespaces or non-alphanumeric characters
                    will be cleaned out prior to processing.

                Returns:
                    lat (float): latitude
                    lon (float): longitude
    
Modules:

    show_zones():

        Utility function to show which zones are currently supported
        by querying the parameters table and printing the zone names
   
    get_origin(zone_name: str, grid_letters: str) -> tuple[int, int]:

        Gets the origin (x0, y0) for the specified zone
        and grid square to calculate the actual position in meters.
        If no such grid is found in that zone, None is returned.

        Paramters:
            zone_name (str): Name of the map zone
            grid_letters (str): Two-letter grid reference
        
        Returns:
            x0 (int): Easting for the grid origin in meters
            y0 (int): Northing for the grid origin in meters

    parse_gridsquare(grid_square: str) -> tuple[str, str, int, int]:

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
    
    gen_crs() -> dict:

        Load CRS string parameters from database and return dictionary of CRS objects

        Returns:
            dictionary of the CRS objects where the key is the map zone and the value
            is the CRS object

    EN_from_grid(zone_name: str, grid: str,x:int,y:int, print_warnings=True) -> tuple[int, int]:

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

    get_lat_lon(zone_name: str, crs_dict: dict, E: int, N: int) -> tuple[float, float]:
  
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
        
    grid_search(x0: int,y0: int, zone_name: str) -> str:
    
        Given the zone and origin, identify the correct grid square
        Return the two-letter grid

        Parameters:
            x0 (int): Easting of the grid's origin
            y0 (int): Northing of the grid's origin
            zone_name (str): Name of the grid

        Return:
            grid (str): Two-letter grid designation

    show_map(lat: float, lon: float):
   
        Takes lat/lon input and searches Google Maps for
        the coordinates, opening a webbrowser page
        in the process.

        Parameters:
            lat (float): latitude in degrees, decimal format
            lon (float): longitude in degrees, decimal format
'''

from .milmapcon import (
    show_zones,
    get_origin,
    parse_gridsquare,
    gen_crs,
    EN_from_grid,
    get_lat_lon,
    grid_search,
    show_map,
    Converter
)