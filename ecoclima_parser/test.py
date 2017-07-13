import unittest
import psycopg2
import datetime
import os
import api

db_name = "testdb"
user = "test"
host = "localhost"
password = "test"
test_data_dir = "test-data/"


class TestEcoclimaApi(unittest.TestCase):

    def test_init_all(self):
        api.initall(db_name, user, host, password)
        conn = psycopg2.connect("dbname='" + db_name + "' user='" + user +
                                "' host='" + host + "' password='" + password +
                                "'")
        cur = conn.cursor()
        cur.execute("""SELECT * FROM stations""")
        self.assertEqual(cur.fetchall(), [])
        cur.execute("""SELECT * FROM measures""")
        self.assertEqual(cur.fetchall(), [])
        conn.close()

    def test_init_station(self):
        api.initall(db_name, user, host, password)
        api.initstation(db_name, user, host, password, "name1", 12.3, 14.4,
                                                 "owner1", test_data_dir + "data1.txt")
        api.initstation(db_name, user, host, password, "name2", 12.5, 14.6,
                                                 "owner2", test_data_dir + "data2.txt")
        conn = psycopg2.connect("dbname='" + db_name + "' user='" + user +
                                "' host='" + host + "' password='" + password +
                                "'")
        cur = conn.cursor()
        cur.execute("""SELECT * FROM stations""")
        self.assertEqual(cur.fetchall(), [(1, 'name1', 12.3, 14.4, 'owner1', test_data_dir + 'data1.txt'),
                                          (2, 'name2', 12.5, 14.6, 'owner2', test_data_dir + 'data2.txt')])
        cur.execute("""SELECT * FROM measures""")
        self.assertEqual(cur.fetchall(), [])
        conn.close()

    def test_update(self):
        api.initall(db_name, user, host, password)
        os.rename(test_data_dir + "dataA.txt", test_data_dir + "data1.txt")
        os.rename(test_data_dir + "dataB.txt", test_data_dir + "data2.txt")
        api.initstation(db_name, user, host, password, "name1", 12.3, 14.4, "owner1",
                        test_data_dir + "data1.txt")
        api.initstation(db_name, user, host, password, "name2", 12.5, 14.6, "owner2",
                        test_data_dir + "data2.txt")
        api.update(db_name, user, host, password, test_data_dir + "data1.txt")
        api.update(db_name, user, host, password, test_data_dir + "data2.txt")
        stats = api.getstats(db_name, user, host, password, test_data_dir + "data1.txt", "",
                             datetime.datetime(2017, 7, 5))
        stats2 = api.getstats(db_name, user, host, password, test_data_dir + "data2.txt", "",
                              datetime.datetime(2017, 7, 5))
        os.rename(test_data_dir + "data1.txt", test_data_dir + "dataA.txt")
        os.rename(test_data_dir + "data2.txt", test_data_dir + "dataB.txt")
        self.assertEqual(stats,
                         {'precipitation': 0.0, 'temperature':
                             {'aver': 10.672727281397, 'max': 12.0, 'min': 10.1}})
        self.assertEqual(stats2,
                         {'precipitation': 0.0, 'temperature': {'aver': 10.1439999008179, 'max': 11.7, 'min': 9.6}})

    def test_update2(self):
        api.initall(db_name, user, host, password)
        os.rename(test_data_dir + "dataA.txt", test_data_dir + "data1.txt")
        api.initstation(db_name, user, host, password, "name1", 12.3, 14.4,
                        "owner1", test_data_dir + "data1.txt")
        api.initstation(db_name, user, host, password, "name2", 12.5, 14.6,
                        "owner2", test_data_dir + "data2.txt")
        api.update(db_name, user, host, password, test_data_dir + "data1.txt")
        stats = api.getstats(db_name, user, host, password, test_data_dir + "data1.txt", "",
                             datetime.datetime(2017, 7, 5))
        os.rename(test_data_dir + "data1.txt", test_data_dir + "dataA.txt")
        os.rename(test_data_dir + "dataB.txt", test_data_dir + "data1.txt")
        api.update(db_name, user, host, password, test_data_dir + "data1.txt")
        stats2 = api.getstats(db_name, user, host, password, test_data_dir + "data1.txt", "",
                              datetime.datetime(2017, 7, 5))
        stats3 = api.getstats(db_name, user, host, password, test_data_dir + "data2.txt", "",
                              datetime.datetime(2017, 7, 5))
        os.rename(test_data_dir + "data1.txt", test_data_dir + "dataB.txt")
        self.assertEqual(stats,
                         {'precipitation': 0.0, 'temperature':
                             {'aver': 10.672727281397, 'max': 12.0, 'min': 10.1}})
        self.assertEqual(stats2,   {'precipitation': 0.0, 'temperature':
            {'aver': 10.4249999523163, 'max': 12.0, 'min': 9.6}})
        self.assertEqual(stats3, {'precipitation': None, 'temperature':
            {'aver': None, 'max': None, 'min': None}})


if __name__ == '__main__':
    unittest.main()
