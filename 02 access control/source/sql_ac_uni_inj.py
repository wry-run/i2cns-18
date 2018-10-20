# https://stackabuse.com/a-sqlite-tutorial-with-python/

import os
import sqlite3


do_create_tables = True
do_create_content = True

connection = sqlite3.connect('uni.db')
cursor = connection.cursor()

cursor.execute("""PRAGMA foreign_keys = ON""")

#for row in cursor.execute("pragma table_info('users')").fetchall():
#		print row

if do_create_tables:

	create_tables = """
		CREATE TABLE IF NOT EXISTS roles (
		name text NOT NULL,
		permission text NOT NULL);


		CREATE TABLE IF NOT EXISTS users (
		name text NOT NULL,
		role text NOT NULL)"""

	cursor.executescript(create_tables)
	
	# sanity check
	
	for row in cursor.execute("pragma table_info('users')").fetchall():
		print row

	for row in cursor.execute("pragma table_info('roles')").fetchall():
		print row

	# connection.commit()


if do_create_content:

	RA = [ ['"PCMember"', '"GrantTenure"'], ['"Faculty"', '"AssignGrades"'], ['"TA"', '"AssignHWScores"'], ['"UEmployee"','"ReceiveBenefits"'], ['"Student"', '"UseGym"'], ['"UMember"','"UseGym"'] ]

	UA = [ ['"Alice"', '"PCMember"'], ['"Bob"', '"Faculty"'], ['"Charlie"', '"Faculty"']]

	for entry in RA:

		cursor.execute("""insert into roles (name, permission) values ({0}, {1})""".format(entry[0], entry[1]))

	select_roles = "select * from roles"
	cursor.execute(select_roles)
	print 'All roles: {0}'.format( cursor.fetchall() )

	for entry in UA:
		
		cursor.execute("""insert into users (name, role) values ({0}, {1})""".format(entry[0], entry[1]))

	

	select_users = "select * from users"
	cursor.execute(select_users)
	print 'All users: {0}'.format(cursor.fetchall())


# user registration



new_user_from_http_form = '"David"'
new_user_role_assigned_by_system = '"Student"'

cursor.execute("""insert into users (name, role) values ({0}, {1})""".format(new_user_from_http_form, new_user_role_assigned_by_system))



select_users = "select * from users"
cursor.execute(select_users)
print 'All users after registration of David: {0}'.format(cursor.fetchall())


new_user_from_http_form = '"Eve; DROP TABLE users"'
new_user_role_assigned_by_system = '"Student"'

cursor.executescript("""insert into users (name, role) values ({0}, {1})""".format(new_user_from_http_form, new_user_role_assigned_by_system))


select_users = "select * from users"
cursor.executescript(select_users)
print 'All users after registration of Eve: {0}'.format(cursor.fetchall())

# connection.close()



