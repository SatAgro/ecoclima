# Ecoclima
Parsing tool and library for Ecoclima meteorological stations (https://stacjameteo.com/)

## Installation

For the use of the library Postgres data base is required a long with python client libraries.
 
    sudo apt-get update
    sudo apt-get install postgresql python3-pip virtualenv

Before use and isntall the library we strongly recommend the creation of a virtual env.

 
And finally install the library by typing:
 
    pip3 install --upgrade virtualenv virtualenvwrapper
    
    mkdir $HOME/.virtualenvs
    echo export WORKON_HOME=$HOME/.virtualenvs >> $HOME/.bashrc
    echo source /usr/local/bin/virtualenvwrapper.sh  >> $HOME/.bashrc
    
    source $HOME/.bashrc

    virtualenv -p python3 $HOME/.virtualenvs/ecoclima
    workon ecoclima
    
    pip3 install psycopg2
    python setup.py install
    
## DB creation

The library store all parsed data into an Postgres data base. To create it just type:

    export PGDATABASE=ecoclima
    export PGUSER=$USER
    export PGPASSWORD=ecoclima
    sudo -u postgres psql <<EOF
    CREATE DATABASE ${PGDATABASE};
    \c ${PGDATABASE}
    CREATE EXTENSION postgis;
    CREATE USER ${PGUSER} with password '${PGPASSWORD}';
    ALTER ROLE ${PGUSER} SET client_encoding TO 'utf8';
    ALTER ROLE ${PGUSER} SET default_transaction_isolation TO 'read committed';
    ALTER ROLE ${PGUSER} SET timezone TO 'UTC';
    GRANT ALL PRIVILEGES ON DATABASE ${PGDATABASE} TO ${PGUSER};
    EOF
    
 ## Usage
    cd ecoclima_parser
    
    # create or clear both tables
    python init_all.py $PGDATABASE $PGUSER localhost $PGPASSWORD
    
    # create or update station of given file path (or url)
    python init_station.py $PGDATABASE $PGUSER localhost $PGPASSWORD station_name lat lon owner url_or_file_path
    
    # update the table with data from station given by file path/url or name
    # when neither url nor name is given, all stations are updated
    python update.py $PGDATABASE $PGUSER localhost $PGPASSWORD [-p url_or_file_path] [-n station_name]
    
    # stats of today
    python api.py $PGDATABASE $PGUSER localhost $PGPASSWORD [-p url_or_file_path] [-n station_name]

## Usage from python script
    from ecoclima_parser import api
    api.initall(db_name, user, host, password, file_path)
    api.initstation(db_name, user, host, password, station_name, lat, lon, owner, file_path)
    api.update(db_name, user, host, password, file_path)
    
    # get stats of the day
    # when stations is given by name, file_path sould be ''
    api.getstats(db_name, user, host, password, file_path [, station_name, datetime])
    
## tests
    cd ecoclima_parser
    sh prepare_to_tests.sh
    python test.py
