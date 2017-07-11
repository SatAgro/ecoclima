import init_all
import update_table
import init_station
import psycopg2
import sys
import datetime
from datetime import datetime


def initall(db_name, user, host, password):
    init_all.init_all(db_name, user, host, password)


def initstation(db_name, user, host, password, name, lat, lon, owner, url):
    init_station.init_station(db_name, user, host, password, name, lat, lon, owner, url)


def updatetable(db_name, user, host, password, file_path):
    update_table.update_table(db_name, user, host, password, file_path)


def getstats(db_name, user, host, password, file_path, dt=datetime.today()):

    try:
        conn = psycopg2.connect("dbname='" + db_name + "' user='" + user +
                                "' host='" + host + "' password='" + password +
                                "'")
        cur = conn.cursor()
        cur.execute("""SELECT id FROM stations WHERE url='""" + file_path + """'""")
        station_id = cur.fetchone()[0]
        dts = datetime.strftime(dt, "%Y-%m-%d")
        cur.execute("""SELECT MIN(low_temp) FROM measures WHERE station_id=""" + str(station_id) + """ and m_date='""" + dts + """'""")
        min_temp = cur.fetchone()[0]
        cur.execute("""SELECT MAX(hi_temp) FROM measures WHERE station_id=""" + str(station_id) + """ and m_date='""" + dts + """'""")
        max_temp = cur.fetchone()[0]
        cur.execute("""SELECT AVG(temp_out) FROM measures WHERE station_id=""" + str(station_id) + """ and m_date='""" + dts + """'""")
        aver_temp = cur.fetchone()[0]
        cur.execute("""SELECT SUM(rain) FROM measures WHERE station_id=""" + str(station_id) + """ and m_date='""" + dts + """'""")
        rain_sum = cur.fetchone()[0]

        cur.close()
        conn.commit()
        conn.close()
        return {"precipitation": rain_sum,
                "temperature": {"min": min_temp, "max": max_temp, "aver": aver_temp}}
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

if __name__ == '__main__':
    print getstats(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5])


