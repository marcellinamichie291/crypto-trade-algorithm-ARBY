#!/usr/local/bin/python3

import warnings
from concurrent.futures import ThreadPoolExecutor, as_completed
from psycopg2.pool import ThreadedConnectionPool
import psycopg2 as pg
import ccxt, numpy as np, time, threading#, numpy.core.defchararray as np_f
from coinmarketcap import Market
from collections import Counter # Counter counts the number of occurrences of each itemf
warnings.simplefilter(action='ignore', category=FutureWarning)
import random
import sys
import multiprocessing
import threading

from serverSETTING import ipaddress


class pglaSTATUS(): #THIS DATABASE IS THE WHEEL.
	def __init__(self):
		self.login_info = f"dbname='status' user= 'postgres' host='{ipaddress}' password='*' port='5432'"
		print(f'Successfully connected to database.')	

	def deleteAll(self):
		connection = pg.connect(self.login_info)
		connection.autocommit = True		
		cursor = connection.cursor()
		cursor.execute(""" select relname from pg_class where relkind='r' and relname !~ '^(pg_|sql_)'; """)
		tables = cursor.fetchall()

		for table in tables:
			cursor.execute(f""" DROP TABLE "{table[0]}" """)
			print(f'Successfully deleted the {table[0]} table from database!')
		connection.close()

	def setup(self):
		connection = pg.connect(self.login_info)
		connection.autocommit = True		
		cursor = connection.cursor()
		cursor.execute(f""" CREATE TABLE "status"(id serial PRIMARY KEY, status varchar) """)
		cursor.execute(f""" INSERT INTO "status"(status) VALUES ('Online') """)
		print('Successfully created a STATUS table!')

	def offline(self):
		connection = pg.connect(self.login_info)
		connection.autocommit = True
		cursor = connection.cursor()
		cursor.execute(f""" UPDATE "status" SET status='Offline' WHERE status='Online' """)
		connection.close()
		print('Sent message to shutdown database!')		

	def online(self):
		connection = pg.connect(self.login_info)
		connection.autocommit = True
		cursor = connection.cursor()
		cursor.execute(f""" UPDATE "status" SET status='Online' WHERE status='Offline' """)
		connection.close()
		print('Sent message to restart database!')	

	def fetchMemoryTags(self):
		connection = pg.connect(self.login_info)
		connection.autocommit = True		
		cursor = connection.cursor()
		cursor.execute(""" select relname from pg_class where relkind='r' and relname !~ '^(pg_|sql_)'; """)
		alltables = np.array(cursor.fetchall())
		alltables = alltables.flatten()
		connection.close()
		return alltables

	def fetch(self):
		connection = pg.connect(self.login_info)
		connection.autocommit = True
		cursor = connection.cursor()
		cursor.execute(f""" SELECT * FROM "status" """)
		result = cursor.fetchall()
		connection.close()
		#print(f'Fetched online PGLA! -> {result}')
		return result[0][1]

if __name__ == '__main__':
	status = pglaSTATUS()