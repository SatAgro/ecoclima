# ecoclima
Parsing tool and library for Ecoclima meteorological stations (https://stacjameteo.com/)

## installation
    sudo apt-get update
    sudo apt-get install postgresql
    pip install psycopg2
    python setup.py install

## usage
    cd ecoclima_parser
    
    # create or clear table
    python init_table db_name user host password table_name
    
    # update the table with data from file (or url)
    python update_table db_name user host password table_name file

## usage from python script:
    from ecoclima_parser import api
    api.inittable(db_name, user, host, password, table_name)
    api.updatetable(db_name, user, host, password, table_name, file)
    
    # get stats of the day
    api.getstats(db_name, user, host, password, table_name, datetime)
