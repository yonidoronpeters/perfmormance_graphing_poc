import json
import datetime as dt
import MySQLdb
import pandas as pd
import pandas.io.sql as sql
import os
import time

DAY_IN_SEC = 60 * 60 * 24

def generate_perf_numbers(days=7, batch_size=1000000):
    df = get_dataframe(days, batch_size)
    df.rename(columns={'database_machine': 'database', 'TPS_Combined': 'TPS', 'dataload_start': 'start_time'}, inplace=True); # rename the column headers
    print(df)
    clean_the_data(df)
    dates = map(str, df.drop_duplicates(subset='start_time')['start_time'].tolist()) # can also use today.strftime('%m/%d/%y')
    grouped = df.pivot_table(index = 'start_time', columns = 'database', values = 'TPS') # pivot the dataframe
    grouped['avg'] = grouped.mean(numeric_only = True, axis=1) # add an avg for each row (only for present values)
    grouped_dict = grouped.fillna(value = 0).to_dict('list') # replace NaN with 0 and turn to a dictionary
    for key,lst in grouped_dict.iteritems():
        lst.insert(0, key)
    grouped_dict['dates']= dates
    write_to_file(grouped_dict)
    print(df)

def write_to_file(grouped_dict):
    filename = 'json/data.json'
    if not os.path.exists(os.path.dirname(filename)):
        try:
            os.makedirs(os.path.dirname(filename))
        except OSError as exc: # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise
    with open(filename, 'w') as outfile:
        json.dump(grouped_dict, outfile)

def get_dataframe(days, batch_size):
    # get db connection and execute query
    conn = MySQLdb.connect(host=os.environ['HOST'], user=os.environ['USER'], passwd=os.environ['PASSWD'], db=os.environ['DB_NAME'])
    return sql.read_sql(query(days, batch_size), conn)

def query(days, batch_size):
    select = 'select database_machine, TPS_Combined, dataload_start'
    frm = ' from metrics'
    where = ' where load_size = ' + str(batch_size) + ' and dataload_start >= DATE_SUB(NOW(), INTERVAL ' + str(days) + ' day)'
    order_by = ' order by dataload_start'
    return select + frm + where + order_by

def db_name(url):
    return str(url).split(":")[1]

def clean_the_data(df):
    df['database'] = df['database'].apply(db_name)
    df['start_time'] = df['start_time'].dt.date

if __name__ == "__main__":
    while True:
        generate_perf_numbers(11)
        time.sleep(DAY_IN_SEC)
