from flask import Flask, render_template, url_for, session, request, redirect
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user, current_user
from collections import OrderedDict
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
import os
import string
import csv
import binascii

app = Flask(__name__)

app.debug = True
app.config['ENV'] = 'development'
app.secret_key = ''.join(str(r) for r in os.urandom(32))


# flask-login

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = '/login/'
login_manager.login_message = u"This is not the page you're looking for."

# simple text file as database

user_db =  os.getcwd() + '/user.tsv'
# user db schema:
# id	name	hashword	salt


salt_length = 16
id_length = 16

hash_function = hashes.SHA256()

# pass a list of page names to html templates to automatically create links

def make_headers():

	if current_user.is_authenticated:

		header_list = ['Home', 'Private', 'Logout']
	else:

		header_list = ['Home', 'Login', 'Register']

	header_dict = OrderedDict()

	header_urls = [url_for(j.lower()) for j in header_list]
	for j in range(len(header_list)):
		header_dict[header_list[j]] = header_urls[j]

	return header_list, header_dict


# user model
class User(UserMixin):

	def __init__(self, uid, username):
		self.id = uid
		self.name = username
		
	def __repr__(self):
		return 'ID: {0}\nName: {1}'.format(self.id, self.name)


# check whether requested user name already exists
def username_exists(username):

	with open(user_db,'r') as tsvin:
		tsvin = csv.reader(tsvin, delimiter='\t', quoting=csv.QUOTE_NONE)
		for row in tsvin:
			if row[1]==username:
				return True
	return False


def username_by_uid(uid):

	with open(user_db,'r') as tsvin:
		tsvin = csv.reader(tsvin, delimiter='\t', quoting=csv.QUOTE_NONE)
		for row in tsvin:
			if row[0]==uid:
				return row[1]
	return False


def password_hash(password, salt):
	digest = hashes.Hash(hash_function, backend=default_backend())
	digest.update(binascii.a2b_base64(password + salt))
	hashword = digest.finalize()
	return binascii.b2a_base64(hashword)


def user_register(username, password):
	# TODO cactch possible file errors here
	
	with open(user_db,'a') as tsvout:
		
		uid = binascii.b2a_base64(os.urandom(id_length)).rstrip()
		salt = binascii.b2a_base64(os.urandom(salt_length)).rstrip()
		hashword = password_hash(password, salt).rstrip()
		entry = [uid, username, hashword, salt]
		for item in entry:
			tsvout.write(item + '\t')
		tsvout.write('\n')

# check whether requested user name exists; if so, retrieve salt and stored password
def user_login_authorize(username, claimed_password):
	
	with open(user_db,'r') as tsvin:
		tsvin = csv.reader(tsvin, delimiter='\t')
		for row in tsvin:
			if row[1]==username:
				stored_hashword = row[2]
				salt = row[3]
				computed_hashword = password_hash(claimed_password, salt).rstrip()

				if computed_hashword == stored_hashword:
					return row[0]

	return False



@login_manager.user_loader
def load_user(user_id):
    return User(user_id, username_by_uid(user_id))


@app.route('/login/', methods=['GET', 'POST'])
def login():

	if request.method == 'POST':
		username = request.form['username']
		password = request.form['password']

		uid = user_login_authorize(username, password)
		
		if uid is not False:
			
			user = User(uid, username)
			
			login_user(user)

			next = request.args.get('next')

		return redirect(url_for('private'))
	
	header_list, header_dict = make_headers()
	return render_template('login_form.html', header_list=header_list, header_active='Login', header_dict=header_dict)



@app.route('/register/', methods=('GET', 'POST'))
def register():
	if request.method == 'POST':
		username = request.form['username']
		password = request.form['password']

		error = None

		if not username:
			error = 'Username is required.'
		elif not password:
			error = 'Password is required.'
		elif username_exists(username):
			error = 'User {} is already registered.'.format(username)

		if error is None:
		
			user_register(username, password)
			return redirect(url_for('private'))


	header_list, header_dict = make_headers()

	return render_template('register.html', header_list=header_list, header_active='Register', header_dict=header_dict)



@app.route('/')
@app.route('/home/')
def home():

	header_list, header_dict = make_headers()

	return render_template('layout.html', header_list=header_list, header_active='Home', header_dict=header_dict)



@app.route('/private/')
@login_required
def private():
	
	header_list, header_dict = make_headers()

	return render_template('private.html', header_list=header_list, header_active='Private', header_dict=header_dict)


@app.route('/logout/')
@login_required
def logout():
    logout_user()
    return redirect('/')


if __name__ == '__main__':
		
	app.run( port=5001, host='0.0.0.0' )


