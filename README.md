# milmapcon

milmapcon (Military Map Converter) is a Python library (built using [pyproj](https://pyproj4.github.io/pyproj/stable/index.html)) which converts 4 or 6 digit grid coordinates from WWII-era maps into latitude and longitude coordinates in the [WGS 84](https://en.wikipedia.org/wiki/World_Geodetic_System) coordinate system. milmapcon can be installed using [pip](https://pip.pypa.io/en/stable/):

```bash
pip install milmapcon
```
## Usage
milmapcon supports the following grid systems which were used in the European Theatre of Operations during WWII:

* British Cassini Grid
* Irish Cassini Grid
* French Lambert Zones 1-3
* Northern European Zone 3
* Nord de Guerre Zone
* Iberian Peninsula Zone
* North Italy Zone
* South Italy Zone

More information on these grids can be found on [Thierry Arsicaud's website](https://www.echodelta.net/mbs/eng-overview.php) which heavily influenced this project. This library is not meant to provide extremely high-precision conversions, but should nevertheless be useful in producing reasonably accurate maps especially if the results are cross-checked against other resources such as original maps or primary-source descriptions of terrain, etc.

Basic usage of the library is as follows:

```python
import milmapcon as mmc

zone_name = "nord_de_guerre"
grid_ref = "vS014448"   # approximate position of the Arc de Triomphe

converter = mmc.Converter(zone_name, print_warnings=True)

lat, lon = converter.convert(grid_ref)
# returns (48.87381346581111, 2.295301091901731)
```
The library has a very basic utilty to display the coordinates in a [GoogleMaps](https://google.com/maps/search/?api=1&query=48.8747757375431,2.2965631977684913) page using Python's builtin webbrowser library:
```python
mmc.show_map(lat, lon)
# opens your browser to a Google map page with a pin on these coordinates
```
>
![screenshot](map_demo.jpg)
>
The library also has a function which lists all zones currently supported. More importantly, it lists the exact strings which should be used in specifying the zone (as shown above):
```python
mmc.show_zones()
```

Prints the following list:
>
    1). "british_cassini"
    2). "french_lambert_1
    3). "french_lambert_2"
    4). "french_lambert_3"
    5). "iberian"
    6). "irish_cassini"
    7). "italy_north"
    8). "italy_south"
    9). "nord_de_guerre"
    10). "north_euro_3
>

Note the `print_warnings` option upon initializing the Converter class. Leaving this set to the default of `True` will provide some indication as to why the specified grid reference could not be converted successfully. However, the conversion function will also return `None` for lat/lon in the event a conversion fails. For example, if you wanted to convert a large number of coordinates, you may wish to suppress the warnings and simply rely on the `None` values to flag coordinates which couldn't be converted.

A practical use of this might be in converting a `pandas` dataframe which contains a series of coordinates (example usage below): 

```python
import pandas as pd
import milmapcon as mmc

coord_df    # assume we've populated a dataframe of our grid references
            # and that the grid reference is in the "grid_ref" column

# Option 1 - converting a series of references in the same zone

zone_name = 'nord_de_guerre'
converter = mmc.Converter(zone_name)

def convert_1(grid_ref):
    '''
    Custom function to use with pandas apply
    '''
    lat, lon = converter.convert(grid_ref)
    return f'{lat},{lon}'

coord_df['lat/lon'] = coord_df['grid_ref'].apply(lambda x: convert_1(x))

# Option 2 - converting grids in multiple zones where the zone is a
# separate column of the dataframe

def convert_2(zone, grid_ref):
    converter = mmc.Converter(zone_name)
    lat, lon = converter.convert(grid_ref)
    return f'{lat},{lon}'

coord_df['lat/lon'] = coord_df.apply(
                lambda row: convert_2(row['zone'], row['grid_ref']), axis=1)
```
Here I chose to return the coordinates to the dataframe as comma-delimited strings which could be parsed out into separate columns, converted back to float, etc. It's also worth noting that this approach may not be highly performant if the dataframe is large, but should handle hundreds (or even thousands) of rows without too much difficulty. The main advantage here is getting the data in a format that can be used in something like `geopandas`, for creating custom maps.

## Other technical considerations

Successful use of this library requires you to know the map zone in which a given grid square reference exists. Fortunately there are a few excellent resources which can help:

1.  [echodelta.net](https://www.echodelta.net/mbs/eng-overview.php) - This site by Thierry Arsicaud provides a lot of information about these old coordinate systems and also includes an online [coordinates translator](https://www.echodelta.net/mbs/eng-translator.php) which can be used as well. As noted above, this site was used as a primary source of research for defining the coordinate transformations.
2. [McMaster University Library](https://library.mcmaster.ca/wwii-topographic-map-series#tab-wwii-topographic-map-series) - has made high-quality scans of period maps available to download. These were indispensible for obtaining technical map data such as the natural origins, projections, grid square origins, and false coordinates of the origin.
3. [UT Austin Libraries](https://maps.lib.utexas.edu/maps/ams/) - has similarly made a large number of maps available from the U.S. Army Map Service. These scans are also of very high quality.

## Adding more maps

In since the calculations are done using the pyproj library, it is possible to add additional zones to this library. Please contact me if you are interested. For each zone additional zone, the following data would be required:
* Understanding of all two-letter (100 km) grids in the zone, and their relation to one another, for the purposes of programming the origins for each grid.
* Data pertinent for defining the coordinate system in pyproj. Namely:
    * Type of projection (i.e. Cassini Solder, Lambert Conformal, etc.)
    * Coordinates of the natural origin
    * False coordinates (Easting, Northing) of the natural origin
    * The reference ellipsoid (i.e. Bessel, Airy, etc.) or the underlying parameters which define them such as the radius of major/minor axis ($a, b$), inverse flattening ($1/f$), scaling factor ($k_0$)

The data for the supported projections are packaged with the library as a sqlite3 database, but will also be made available on the [GitHub](https://github.com/mkershis/milmapcon) repository for this project in `csv format.