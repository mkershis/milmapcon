# milmapcon database schema
milmapcon is packaged with a SQL database (sqlite3) which contains all the parameters needed to perform the coordinate transformations. This database is packaged with the library as `gs_data.db`.

The database contains the following two tables:

### origins

The origins table is built such that the zone-grid combinations are unique. The `update_db.py` script updates the database using `INSERT OR REPLACE` so there will be no duplicates, but previous values can be overwritten in case errors need to be corrected, for example.

|Field|Description|Type|
|-----|-----------|----|
|`zone` |Map zone. See "show_zones()" function for allowable values|`TEXT`|
|`grid` |Two-letter grid identifier|`TEXT`|
|`x0`|Easting of the grid origin in meters|`INTEGER`|
|`y0`|Northing of the grid origin in meters|`INTEGER`|

### parameters

The parameters table is built such that only the zone is unique as this table contains the parameters 

|Field|Description|Type|
|-----|-----------|----|
|`zone`|Map zone. See "show_zones()" function for allowable values|`TEXT`|
|`proj`|[Projection](https://proj.org/en/stable/operations/projections/index.html) to be used in the coordinate transformation|`TEXT`|
|`lat_0`|Latitude in degrees (decimal) of the natural origin |`TEXT`|
|`lon_0`|Longitude in degrees (decimal) of the natural origin|`TEXT`|
|`x_0`|False Easting of the natural origin|`TEXT`|
|`y_0`|False Northing of the natural origin|`TEXT`|
|`a`|Radius of major axis of ellipsoid in meters |`TEXT`|
|`rf`|Inverse flattening ($1/f$)|`TEXT`|
|`k_0`|Scaling factor. Optional, can be `NULL`|`TEXT`|
|`ellps`|Name of [reference ellipsoid](https://proj.org/en/stable/usage/ellipsoids.html#built-in-ellipsoid-definitions) if using instead of defining $a$ and $1/f$. If this parameter is defined then $a$ and $1/f$ would be `NULL` values|`TEXT`|

## Adding additional maps

Adding additional transformations to the milmapcon library can be easily accomplished by updating *both* tables with the necessary data. The `origins` table cannot have any `NULL` values whereas the `parameters` table can take null values for $a$, $1/f$, or $k_0$ if the reference ellipsoid is being defined by name instead.