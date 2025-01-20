'''
This script can be used to populate (or repopulate) the database
with either new grids or new parameters. You'll note that the query
is written to INSERT or REPLACE which means it will insert new data
and overwrite old data if you try to insert a duplicate. 
'''

import sqlite3
import csv
import gridsquare as gs
from pathlib import Path

origin_dir = Path(Path(__file__).parent, 'origins.csv')
param_dir = Path(Path(__file__).parent, 'crs_params.csv')
db_dir = Path(Path(__file__).parent, 'gs_data.db')


with sqlite3.connect(db_dir) as con:
    cur = con.cursor()

    with open(origin_dir, encoding='utf-8-sig') as file:
        csv_linereader = csv.reader(file, delimiter=',')
        next(csv_linereader) # skip header
        for row in csv_linereader:
            zone, grid, x0, y0 = row

            cur.execute(f''' 
            INSERT OR REPLACE INTO origins
                VALUES('{zone}','{grid}',{int(x0)},{int(y0)})
            ''')
    
    con.commit()

with sqlite3.connect(db_dir) as con:
    cur = con.cursor()
    
    with open(param_dir, encoding='utf-8-sig') as file:
        csv_linereader = csv.reader(file, delimiter=',')
        next(csv_linereader) # skip header
        for row in csv_linereader:
            zone, proj, lat_0, lon_0, x_0, y_0, a, rf, k_0, ellps = row

            cur.execute(f''' 
            INSERT OR REPLACE INTO parameters
                VALUES('{zone}','{proj}','{lat_0}','{lon_0}','{x_0}','{y_0}','{a}','{rf}','{k_0}','{ellps}')
            ''')
    con.commit()