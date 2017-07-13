#!/usr/bin/python
# -*- coding: utf-8 -*-

import argparse
import psycopg2
import sys
if sys.version_info[0] == 3:
    from urllib.request import urlopen
else:
    from urllib import urlopen


def date_text(value):
    return """, to_date('""" + value + """', 'YY-MM-DD')"""


def val_text(value):
    if ':' in value:
        return """, to_timestamp('""" + value + """', 'HH24:MI')::time"""
    elif '.' in value or value.isdigit():
        return """, """ + value
    elif '---' in value:
        return """, null"""
    else:
        return """, '""" + value + """'"""


def update(db_name, user, host, password, file_path='', station_name=''):
    if file_path == '' and station_name == '':
        try:
            conn = psycopg2.connect("dbname='" + db_name + "' user='" + user +
                                    "' host='" + host + "' password='" + password +
                                    "'")
            cur = conn.cursor()
            cur.execute("""SELECT url FROM stations""")
            res = cur.fetchall()
            for el in res:
                if not update(db_name, user, host, password, el[0]):
                    return False
            return True

        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
    elif file_path == '':
        try:
            conn = psycopg2.connect("dbname='" + db_name + "' user='" + user +
                                    "' host='" + host + "' password='" + password +
                                    "'")
            cur = conn.cursor()
            cur.execute("""SELECT url FROM stations WHERE name='""" + station_name + """'""")

            try:
                file_path = cur.fetchone()[0]
            except (Exception, psycopg2.DatabaseError) as error:
                print("name doesn't exist")
                return False

        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

    try:
        f = open(file_path, "r")
        lines = f.readlines()
    except IOError:
        f = urlopen(file_path)
        lines = f.readlines()
        lines = list(map(lambda x: x.decode('ascii'), lines))

    for _ in range(3):
        lines.pop(0)

    try:
        conn = psycopg2.connect("dbname='" + db_name + "' user='" + user +
                                "' host='" + host + "' password='" + password +
                                "'")
        cur = conn.cursor()
        cur.execute("""SELECT id FROM stations WHERE url='""" + file_path + """'""")
        station_id = cur.fetchone()[0]
        for line in lines:
            values = line.split()
            cur.execute(""" DELETE FROM measures""" +
                        """ WHERE station_id=""" + str(station_id) + """and m_date=to_date('""" + values[0] +
                        """', 'YY-MM-DD') and m_time=to_timestamp('""" +
                        values[1] + """', 'HH24:MI')::time
                        """)
            query = """ INSERT INTO measures VALUES (""" + str(station_id) + date_text(values[0])
            values.pop(0)
            for val in values:
                query = query + val_text(val)
            query = query + """)"""
            cur.execute(query)

        # cur.execute("SELECT * FROM " + table_name)
        # print cur.fetchall()

        cur.close()
        conn.commit()
        conn.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    f.close()
    return True

if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('dbname')
    p.add_argument('user')
    p.add_argument('host')
    p.add_argument('passw')
    p.add_argument('-p', '--path', default='')
    p.add_argument('-n', '--name', default='')
    ans = p.parse_args()
    if update(ans.dbname, ans.user, ans.host, ans.passw, ans.path, ans.name):
        print ('data from station has been updated')
    else:
        print ('update failed')

