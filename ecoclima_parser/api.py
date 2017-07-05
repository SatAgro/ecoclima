import init_table
import update_table


def inittable(db_name, user, host, password, table_name):
    init_table.init_table(db_name, user, host, password, table_name)


def updatetable(db_name, user, host, password, table_name, file_path):
    update_table.update_table(db_name, user, host, password, table_name, file_path)

