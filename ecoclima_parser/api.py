import init_table
import update_table
import psycopg2
import datetime
from datetime import datetime


def inittable(db_name, user, host, password, table_name):
    init_table.init_table(db_name, user, host, password, table_name)


def updatetable(db_name, user, host, password, table_name, file_path):
    update_table.update_table(db_name, user, host, password, table_name, file_path)

def getstats(db_name="template1", user="satagro", host="localhost", password="satagro", table_name="tab1", dt=datetime.today()):

    try:
        conn = psycopg2.connect("dbname='" + db_name + "' user='" + user +
                                "' host='" + host + "' password='" + password +
                                "'")
        cur = conn.cursor()
        dts = datetime.strftime(dt, "%Y-%m-%d")
        cur.execute("SELECT MIN(low_temp) FROM " + table_name + " WHERE m_date='" + dts + "'")
        min_temp = cur.fetchone()[0]
        cur.execute("SELECT MAX(hi_temp) FROM " + table_name + " WHERE m_date='" + dts + "'")
        max_temp = cur.fetchone()[0]
        cur.execute("SELECT AVG(temp_out) FROM " + table_name + " WHERE m_date='" + dts + "'")
        aver_temp = cur.fetchone()[0]
        cur.execute("SELECT SUM(rain) FROM " + table_name + " WHERE m_date='" + dts + "'")
        rain_sum = cur.fetchone()[0]

        cur.close()
        conn.commit()
        conn.close()
        return {"precipitation": rain_sum,
                "temperature": {"min": min_temp, "max": max_temp, "aver": aver_temp}}
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

if __name__ == '__main__':
    print getstats()


