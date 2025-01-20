''' 
Following script can be used to build your database with the
grid origins and parameters tables. As you can see, the origins table
must be unique with respect to zone and grid, whereas the
parameters table must be unique with respect to zone only
'''

import sqlite3
from pathlib import Path

with sqlite3.connect(Path(Path(__file__).parent,'gs_data.db')) as con:

    cur = con.cursor()

    cur.execute(''' 
    CREATE TABLE IF NOT EXISTS origins(
        zone TEXT,
        grid TEXT,
        x0 INTEGER,
        y0 INTEGER,
        unique(zone, grid)
        )
    ''')

    cur.execute(''' 
    CREATE TABLE IF NOT EXISTS parameters(
        zone TEXT,
        proj TEXT,
        lat_0 TEXT,
        lon_0 TEXT,
        x_0 TEXT,
        y_0 TEXT,
        a TEXT,
        rf TEXT,
        k_0 TEXT,
        ellps TEXT,
        unique(zone)
        )
    ''')

    con.commit()