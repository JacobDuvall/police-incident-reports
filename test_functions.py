import project0
import pandas as pd
import os


def test_download():
    try:
        url = project0.fetch_incidents('http://normanpd.normanok.gov/'
                                       'filebrowser_download/657/2020-03-01%20Daily%'
                                       '20Incident%20Summary.pdf')
        assert url is not None
        print("passed test download")
    except AssertionError:
        print("failed test download")


def test_database():
    project0.create_db()
    if os.path.isfile('normanpd.db'):
        print("passed test database")
    else:
        print("failed test database")


def test_table():
    try:
        conn = project0.connect_db('normanpd.db')
        table = pd.read_sql_query("SELECT name FROM sqlite_master "
                                  "WHERE type = 'table' AND name = 'incidents'", conn)
        assert table['name'][0] == 'incidents'
        print('passed test table')
    except AssertionError:
        print('failed test table')


def test_status():
    try:
        data = project0.fetch_incidents('http://normanpd.normanok.gov/'
                                           'filebrowser_download/657/2020-03-01%20Daily%'
                                           '20Incident%20Summary.pdf')

        incidents = project0.extract_incidents(data)

        project0.create_db()

        project0.populate_db(incidents)

        status = project0.status()

        march1 = open("march1.txt", "r").read()

        assert status == march1
        print("passed test status")
    except AssertionError:
        print("failed test status")


if __name__ == '__main__':
    test_download()
    test_database()
    test_table()
    test_status()
