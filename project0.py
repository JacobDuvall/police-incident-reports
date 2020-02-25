import urllib.request as urllib
import tempfile
import PyPDF2
import sqlite3
from dateutil.parser import parse
import pandas as pd

# python main.py --incidents
# http://normanpd.normanok.gov/filebrowser_download/657/2020-02-20%20Daily%20Incident%20Summary.pdf


# fetch the incidents from Norman Police incidents pdf
def fetch_incidents(url):
    #url = ("http://normanpd.normanok.gov/filebrowser_download/"
    #       "657/2020-02-20%20Daily%20Incident%20Summary.pdf")

    return urllib.urlopen(url).read()


# extract incidents from the Norman Police incidents pdf
def extract_incidents(data):
    fp = tempfile.TemporaryFile()

    # Write the pdf data to a temp file
    fp.write(data)

    # Set the curser of the file back to the begining
    fp.seek(0)

    # Read the PDF
    pdf_reader = PyPDF2.pdf.PdfFileReader(fp)
    num = pdf_reader.getNumPages()

    # Get the first page
    all_pages = ''
    for i in range(num):
        all_pages = all_pages + pdf_reader.getPage(i).extractText()

    all_pages = format_pages(all_pages)

    return all_pages


# handle edge cases like:
#   - multi line address
#   - no incident included
#   - address is latitude/longitude
#   - remove 'NORMAN POLICE DEPARTMENT' and 'Daily Incident Summary (Public)'
def format_pages(all_pages):

    all_lines = get_lines(all_pages)

    all_lines = fix_edge_lines(all_lines)

    return all_lines


# format from pages to line entries for individual incidents
def get_lines(all_pages):
    all_lines = list()
    line = list()

    entries_split = all_pages.split('\n')  # split entries by new line

    for entry in entries_split:
        if not is_norman_police_or_daily_summary(entry):
            if not is_lat_long(entry):
                if is_date_time(entry):
                    all_lines.append(line)
                    line = list()
                    line.append(entry)
                else:
                    line.append(entry)
                    pass
            else:
                line.append(entry)
                pass

    all_lines = all_lines[1:]  # remove header

    return all_lines


# if address is 2 lines long, compress into 1 line
# if no incident written, report as "No Incident"
# if something else, remove the line item
def fix_edge_lines(all_lines):
    for i in range(len(all_lines)):
        if len(all_lines[i]) == 6:
            all_lines[i][2:4] = [''.join(all_lines[i][2:4])]
        if len(all_lines[i]) == 4:
            all_lines[i].insert(3, 'No Incident')
        if len(all_lines[i]) < 4 or len(all_lines[i]) > 6:
            all_lines[i].remove(all_lines[i])

    return all_lines


# is entry the header for NORMAN POLICE DEPARTMENT or Daily Incident Summary?
def is_norman_police_or_daily_summary(entry):
    if ('NORMAN POLICE DEPARTMENT' in entry) or ('Daily Incident Summary' in entry):
        return True
    else:
        return False


# is entry a latitude or longitude?
def is_lat_long(entry):
    if ';' in entry:  # only seeing ';' char in lat/longs
        return True
    else:
        return False


# is entry a date time?
def is_date_time(entry):
    try:
        parse(entry, fuzzy=False)  # check if date time
        return True
    except ValueError:
        return False


# create database normanpd.db for storing incidents
def create_db():
    conn = connect_db('normanpd.db')
    c = conn.cursor()

    # drop table from database if its there
    # create table incidents
    def create_table():
        try:
            c.execute('DROP TABLE incidents;')
            c.execute('CREATE TABLE IF NOT EXISTS incidents('
                      '  incident_time TEXT'
                      ', incident_number TEXT'
                      ', incident_location TEXT'
                      ', nature TEXT'
                      ', incident_ori TEXT'
                      ');')
            conn.commit()
        except Exception as e:
            print(str(e))

    create_table()


# connect to database
def connect_db(db_name):
    return sqlite3.connect(db_name)


# populate database with incidents
def populate_db(incidents):
    conn = connect_db('normanpd.db')
    c = conn.cursor()
    for incident in incidents:
        c.execute('INSERT INTO incidents (incident_time,'
                   'incident_number, incident_location,'
                   'nature, incident_ori) VALUES '
                   '(?, ?, ?, ?, ?)', (incident[0],
                                       incident[1],
                                       incident[2],
                                       incident[3],
                                       incident[4]))
        conn.commit()


# print nature and the nature count from incidents
def status():
    conn = connect_db('normanpd.db')

    df = pd.read_sql_query('SELECT '
                           '  nature'
                           ', COUNT(nature) '
                           'FROM incidents GROUP BY nature', conn)

    for nature, count in zip(df['nature'], df['COUNT(nature)']):
        print(nature, '|', count, sep='')

