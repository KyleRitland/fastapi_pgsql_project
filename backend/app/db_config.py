#from sqlalchemy import create_engine
#from sqlalchemy.ext.declarative import declarative_base
#from sqlalchemy.orm import sessionmaker

import psycopg2
from psycopg2 import OperationalError
from psycopg2.extras import execute_values

from pgvector.psycopg2 import register_vector
import numpy as np


''' 

Code to create database

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


def create_connection():
    DB_connection = psycopg2.connect(
        database="postgres", 
        user='postgres', 
        password='awe68f4asd5v63a1er98g', 
        host='127.0.0.1', 
        port= '5432'
        )

    c = DB_connection.cursor()

    DB_connection.commit()
    
    create_tweets_table(c)
    create_word_counts_table(c) 

    DB_connection.commit()
    
    with open('tweets_df.csv') as csv_file:
        c.copy_expert("COPY tweets FROM STDIN WITH CSV HEADER", csv_file)

    DB_connection.commit()

    with open('word_counts_df.csv', 'r') as f:
        next(f)
        c.copy_from(f, 'word_counts', sep=',')

    DB_connection.commit()

    return DB_connection   

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

