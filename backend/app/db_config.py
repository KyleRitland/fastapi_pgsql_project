#from sqlalchemy import create_engine
#from sqlalchemy.ext.declarative import declarative_base
#from sqlalchemy.orm import sessionmaker

from sqlalchemy import create_engine, MetaData
import io
import csv

'''
import psycopg2


#establishing the connection
conn = psycopg2.connect(
   database="postgres", 
   user='postgres', 
   password='awe68f4asd5v63a1er98g', 
   host='127.0.0.1', 
   port= '5432'
)

conn.autocommit = True

#Creating a cursor object using the cursor() method
cursor = conn.cursor()

#Preparing query to create a database
sql = CREATE DATABASE mydatabase

#Creating a database
cursor.execute(sql)
print("Database created successfully........")

#Closing the connection
conn.close()
'''

#DATABASE_URL = "postgresql+psycopg2://postgres:awe68f4asd5v63a1er98g@localhost:5432/mydatabase"

#database = databases.Database(DATABASE_URL)
#metadata = MetaData()

#engine = create_engine(DATABASE_URL)
#metadata.create_all(engine)

#SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

'''
SQLALCHEMY_DATABASE_URL = "postgresql+psycopg2://user:password@localhost:5432/mydatabase"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, pool_pre_ping=True
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
'''
import psycopg2
from psycopg2 import OperationalError
from psycopg2.extras import execute_values

from pgvector.psycopg2 import register_vector
import numpy as np

def create_connection():
    DB_connection = psycopg2.connect(
        database="postgres", 
        user='postgres', 
        password='awe68f4asd5v63a1er98g', 
        host='127.0.0.1', 
        port= '5432'
        )

    c = DB_connection.cursor()

    #c.execute("CREATE EXTENSION IF NOT EXISTS vector");
    
    DB_connection.commit()
    #register_vector(DB_connection)

    create_tweets_table(c)
    create_word_counts_table(c) 

    DB_connection.commit()
    # Now upload the data as though it was a file

    #data_list = [(int(row['id']), int(row['author_id']), row['created_at'], row['text'], row['text_clean'], np.array(row['embeddings'])) for index, row in df_new.iterrows()]

    #execute_values(c, "INSERT INTO embeddings (title, url, content, tokens, embedding) VALUES %s", data_list)
    import sys

    with open('tweets_df.csv') as csv_file:
        c.copy_expert("COPY tweets FROM STDIN WITH CSV HEADER", csv_file)

    '''with open('tweets_df.csv', 'r') as f:
        next(f)
        c.copy_from(f, 'tweets', sep=',')
        '''
    
    DB_connection.commit()
    with open('word_counts_df.csv', 'r') as f:
        next(f)
        c.copy_from(f, 'word_counts', sep=',')

        
    DB_connection.commit()

    '''
    sql = """SELECT * FROM tweets WHERE created_at BETWEEN '2018-01-01' AND '2018-01-02'"""
    print(sql)
    print(c.execute(sql))
    fetch = c.fetchall()
    print(type(fetch))
    for i in fetch:
        print(i)

    DB_connection.commit()
    '''

    return DB_connection
    #sql = """SELECT * FROM tweets WHERE created_at BETWEEN '2018-01-01' AND '2018-01-02'"""
        

def create_tweets_table(cursor):
    try:
        # Dropping table iris if exists
        cursor.execute("DROP TABLE IF EXISTS tweets;")
        sql = '''CREATE TABLE tweets(
        id INT PRIMARY KEY, 
        author_id BIGINT,
        created_at DATE NOT NULL,
        text_clean VARCHAR(300) NOT NULL,
        embedding decimal[]
        )'''
        # Creating a table
        cursor.execute(sql)
        print("tweets table is created successfully...............")  
    except OperationalError as err:
        # pass exception to function
        print('table creation error tweets: ', err)
        # set the connection to 'None' in case of error
        #conn = None

def create_word_counts_table(cursor):
    try:
        # Dropping table iris if exists
        cursor.execute("DROP TABLE IF EXISTS word_counts;")
        sql = '''CREATE TABLE word_counts(
        id INT PRIMARY KEY,
        word VARCHAR(50) NOT NULL,
        count INT NOT NULL
        )'''
        # Creating a table
        cursor.execute(sql)
        print("word_counts table is created successfully...............")  
    except OperationalError as err:
        # pass exception to function
        print('table creation error word_counts: ', err)
        # set the connection to 'None' in case of error
        #conn = None

