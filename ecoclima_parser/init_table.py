#!/usr/bin/python
# -*- coding: utf-8 -*-

import psycopg2
import sys


def init_table(db_name, user, host, password, table_name):
    try:
        conn = psycopg2.connect("dbname='" + db_name + "' user='" + user +
                                "' host='" + host + "' password='" + password +
                                "'")
        cur = conn.cursor()
        cur.execute("""DROP TABLE IF EXISTS """ + table_name)
        cur.execute("""CREATE TABLE """ + table_name +
                    """(m_date DATE, 
                    m_time TIME, 
                    temp_out REAL,   
                    hi_temp REAL,   
                    low_temp REAL,   
                    out_hum INTEGER,    
                    dew_pt REAL,
                    wind_speed REAL,   
                    wind_dir TEXT,    
                    wind_run REAL, 
                    hi_speed REAL,   
                    hi_dir TEXT,  
                    wind_chill REAL,  
                    heat_index REAL,  
                    thw_index REAL,   
                    bar REAL,
                    rain REAL,  
                    rain_rate REAL, 
                    uv_index REAL,  
                    uv_dose REAL,   
                    hi_uv REAL,     
                    heat_dd REAL,     
                    cool_dd REAL, 
                    in_temp REAL,   
                    in_hum INTEGER,    
                    in_dew REAL,   
                    in_heat REAL,    
                    in_emc REAL, 
                    in_air_density REAL,  
                    soil_moist INTEGER,  
                    soil_temp REAL,  
                    leaf_wet INTEGER, 
                    wind_samp REAL,   
                    wind_tx INTEGER,   
                    iss_recept REAL,  
                    arc_int INTEGER, 
                    CONSTRAINT """ + table_name +
                    """_time_unique UNIQUE (m_date, m_time))""")

        cur.close()
        conn.commit()
        conn.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)


if __name__ == '__main__':
    init_table(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5])
