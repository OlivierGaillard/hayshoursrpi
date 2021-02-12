import os


def get_filepersist():
    """
    - creates the file 'db1' inside directory $ROOTDIR or 'tmp' if undefined
    """
    rootdir = os.getenv("ROOTDIR", "./tmp")
    dbname = "db1"
    from filepersist import FilePersist

    return FilePersist(rootdir, dbname)


def get_sqlpersist():
    """
    - etablish connection with db-server
    - create database and table it they don't exist
    """
    host = "192.168.1.100"
    user = "root"
    password = os.getenv("MARIAPASS")
    port = 30306
    database = "worktime"
    table = "hours"
    from sqlpersist import SQLPersist

    p = SQLPersist(host, user, password, port, database, create=True)
    id_query = "id MEDIUMINT NOT NULL AUTO_INCREMENT"
    primary = "PRIMARY KEY(id)"
    create_table_query = f"""CREATE TABLE {database}.{table}(
        {id_query},
        leaving VARCHAR(10),
        {primary}
        )"""
    p.create_table(create_table_query, table)
    return p
