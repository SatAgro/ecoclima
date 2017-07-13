#!/usr/bin/python
# -*- coding: utf-8 -*-

import psycopg2
import sys


def init_station(db_name, user, host, password, name, lat, lon, owner, url):
    try:
        conn = psycopg2.connect("dbname='" + db_name + "' user='" + user +
                                "' host='" + host + "' password='" + password +
                                "'")
        cur = conn.cursor()
        cur.execute("""DELETE FROM stations WHERE url='""" + url + """'""")
        cur.execute("""INSERT INTO stations (name, lat, lon, owner, url) values ('""" +
                    name + """', """ + str(lat) + """, """ +
                    str(lon) + """, '""" + owner + """', '""" + url + """')""")

        cur.execute("""SELECT * FROM stations""")
        cur.close()
        conn.commit()
        conn.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print (error)
        raise


if __name__ == '__main__':
    init_station(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5],
                 sys.argv[6], sys.argv[7], sys.argv[8], sys.argv[9])
    print ('station has been added')
