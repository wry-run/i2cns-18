# https://stackabuse.com/a-sqlite-tutorial-with-python/

import os
import sqlite3


do_create_tables = False
do_create_content = False

connection = sqlite3.connect('uni.db')
cursor = connection.cursor()

cursor.execute("""PRAGMA foreign_keys = ON""")

#for row in cursor.execute("pragma table_info('users')").fetchall():
#		print row

if do_create_tables:

	create_roles = """
		CREATE TABLE IF NOT EXISTS roles (
		id integer PRIMARY KEY,
		name text NOT NULL UNIQUE,
		permission text NOT NULL)"""

	cursor.execute(create_roles)
	
	create_users = """
		CREATE TABLE IF NOT EXISTS users (
		id integer PRIMARY KEY,
		name text NOT NULL UNIQUE,
		role text NOT NULL,
		FOREIGN KEY (name) REFERENCES roles (name))"""

	cursor.execute(create_users)
	
	# sanity check
	
	for row in cursor.execute("pragma table_info('users')").fetchall():
		print row

	for row in cursor.execute("pragma table_info('roles')").fetchall():
		print row

	# connection.commit()


if do_create_content:

	try:
		create_user = """insert into users (name, role) values ('player_one', 'Student')"""
		cursor.execute(create_user)
		
	except sqlite3.IntegrityError:
		print 'nope'



	print 'There should not be a user player_one because the Student role does not exist yet and the foreign key condition is being enforced'

	select_users = "select * from users"
	cursor.execute(select_users)
	print cursor.fetchall()

# connection.close()



