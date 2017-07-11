# ecoclima
Parsing tool and library for Ecoclima meteorological stations (https://stacjameteo.com/)

## installation
    sudo apt-get update
    sudo apt-get install postgresql
    pip install psycopg2
    python setup.py install

## usage
    cd ecoclima_parser
    
    # create or clear both tables
    python init_all db_name user host password
    
    # create or update station of given file path (or url)
    python init_station db_name user host password station_name lat lon owner file_path
    
    # update the table with data from file (or url)
    python update db_name user host password file_path

## usage from python script:
    from ecoclima_parser import api
    api.inittable(db_name, user, host, password, file_path)
    api.initstation(db_name, user, host, password, station_name, lat, lon, owner, file_path)
    api.updatetable(db_name, user, host, password, file_path)
    
    # get stats of the day
    api.getstats(db_name, user, host, password, file_path, datetime)
