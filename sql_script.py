import sqlite3 as sql
import pandas as pd


# specify source file
files = {'data/cleaned_poi.csv':'poi.db', 'data/cleaned_resto.csv':'resto.db'}

def insert_data(df,conn):
	# insert rows
	df.to_sql('places',conn, if_exists = 'replace',index=False)
	print('INSERT SUCCESS')

def main():
	for f,db in files.items():
		# connect to db
		conn = sql.connect(db)
		c = conn.cursor()
		df = pd.read_csv(f,index_col=False)
		insert_data(df,conn)

	# QUERIES
	conn = sql.connect('poi.db')
	c = conn.cursor()
	print('aa')
	c.execute('SELECT place_name,place_name_link FROM places')
	for row in c.fetchall()[:5]:
		print(row[0],row[1])
	print('\n')

main()