#!/usr/bin/python
# -*- coding: utf-8 -*-

import psycopg2
import sys


def val_text(value):
    if '-' in value:
        return """to_date('""" + value + """', 'YY-MM-DD')"""
    elif ':' in value:
        return """, to_timestamp('""" + value + """', 'HH24:MI')::time"""
    elif '.' in value or value.isdigit():
        return """, """ + value
    else:
        return """, '""" + value + """'"""


def update_table(db_name, user, host, password, table_name, file_path):
    f = open(file_path, "r")
    lines = f.readlines()
    for _ in range(3):
        lines.pop(0)

    try:
        conn = psycopg2.connect("dbname='" + db_name + "' user='" + user +
                                "' host='" + host + "' password='" + password +
                                "'")
        cur = conn.cursor()
        for line in lines:
            values = line.split()
            cur.execute(""" DELETE FROM """ + table_name +
                        """ WHERE m_date=to_date('""" + values[0] +
                        """', 'YY-MM-DD') and m_time=to_timestamp('""" +
                        values[1] + """', 'HH24:MI')::time
                        """)
            query = """ INSERT INTO """ + table_name + """ VALUES ("""
            for val in values:
                query = query + val_text(val)
            query = query + """)"""
            cur.execute(query)

        #cur.execute("SELECT * FROM " + table_name)
        #print cur.fetchall()

        cur.close()
        conn.commit()
        conn.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

if __name__ == '__main__':
    update_table(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4],
                 sys.argv[5], sys.argv[6])
