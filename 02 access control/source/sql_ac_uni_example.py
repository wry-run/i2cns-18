import os
import sqlite3


do_create_tables = True
do_create_content = True

connection = sqlite3.connect('uni.db')
cursor = connection.cursor()


if do_create_tables:

	create_roles = """
		CREATE TABLE IF NOT EXISTS roles (
		name text NOT NULL UNIQUE,
		permission text NOT NULL)"""

	cursor.execute(create_roles)
	
	create_users = """
		CREATE TABLE IF NOT EXISTS users (
		name text NOT NULL UNIQUE,
		role text NOT NULL,
		FOREIGN KEY (role) REFERENCES roles (name))"""

	cursor.execute(create_users)
	
	# sanity check
	
	for row in cursor.execute("pragma table_info('users')").fetchall():
		print row

	for row in cursor.execute("pragma table_info('roles')").fetchall():
		print row

	# connection.commit()


if do_create_content:

	RA = [ ['"PCMember"', '"GrantTenure"'], 
			['"Faculty"', '"AssignGrades"'], 
			['"TA"', '"AssignHWScores"'], 
			['"UEmployee"','"ReceiveBenefits"'], 
			['"Student"', '"UseGym"'], 
			['"UMember"','"UseGym"'] ]

	UA = [ ['"Alice"', '"PCMember"'], 
			['"Bob"', '"Faculty"'], 
			['"Charlie"', '"Faculty"']]

	for entry in RA:

		cursor.execute("""insert into roles (name, permission) values ({0}, {1})
					""".format(entry[0], entry[1]))

	select_roles = "select * from roles"
	cursor.execute(select_roles)
	print 'All roles: {0}'.format( cursor.fetchall() )

	for entry in UA:
		
		cursor.execute("""insert into users (name, role) values ({0}, {1})
						""".format(entry[0], entry[1]))

	

	select_users = "select * from users"
	cursor.execute(select_users)
	print 'All users: {0}'.format(cursor.fetchall())

# connection.close()



