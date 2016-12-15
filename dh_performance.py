import json
import datetime as dt
import MySQLdb
import pandas as pd
import os
import time

DAY_IN_SEC = 60 * 60 * 24

def generate_perf_numbers(days=7, batch_size=1000000):
    rows = get_rows_from_db(days, batch_size)
    # convert data to panda's dataframe
    df = pd.DataFrame( [[ij for ij in i] for i in rows] )
    df.rename(columns={0: 'database', 1: 'TPS', 2: 'start_time'}, inplace=True); # rename the column headers
    clean_the_data(df)
    dates = map(str, df.drop_duplicates(subset='start_time')['start_time'].tolist()) # can also use today.strftime('%m/%d/%y')
    grouped = df.pivot_table(index = 'start_time', columns = 'database', values = 'TPS') # pivot the dataframe
    grouped['avg'] = grouped.mean(numeric_only = True, axis=1) # add an avg for each row (only for present values)
    grouped_dict = grouped.fillna(value = 0).to_dict('list') # replace NaN with 0 and turn to a dictionary
    for key,lst in grouped_dict.iteritems():
        lst.insert(0, key)
    grouped_dict['dates']= dates
    with open('json/data.json', 'w') as outfile:
        json.dump(grouped_dict, outfile)

    print(df)


def get_rows_from_db(days, batch_size):
    # get db connection and execute query
    conn = MySQLdb.connect(host=os.environ['HOST'], user=os.environ['USER'], passwd=os.environ['PASSWD'], db=os.environ['DB_NAME'])
    cursor = conn.cursor()
    cursor.execute(query(days, batch_size))
    return cursor.fetchall()

def query(days, batch_size):
    select = 'select database_machine, TPS_Combined, dataload_start'
    frm = ' from metrics'
    where = ' where load_size = ' + str(batch_size) + ' and dataload_start >= DATE_SUB(NOW(), INTERVAL ' + str(days) + ' day)'
    order_by = ' order by dataload_start'
    return select + frm + where + order_by

def db_name(url):
    return str(url).split(":")[1].replace('sap', 'hana')

def clean_the_data(df):
    df['database'] = df['database'].apply(db_name)
    df['start_time'] = df['start_time'].dt.date

if __name__ == "__main__":
    while True:
        generate_perf_numbers(11)
        time.sleep(DAY_IN_SEC)
