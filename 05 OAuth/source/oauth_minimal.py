from flask import Flask, redirect, url_for, session
from flask_oauth import OAuth
import os
import urllib2

GOOGLE_CLIENT_ID = '...'
GOOGLE_CLIENT_SECRET = '...'
REDIRECT_URI = '/oauth2redirect'
 
app = Flask(__name__)

app.debug = True
app.config['ENV'] = 'development'
app.secret_key = ''.join(str(r) for r in os.urandom(32))

oauth = OAuth()
 
google = oauth.remote_app('google',
						  base_url='https://www.google.com/accounts/',
						  authorize_url='https://accounts.google.com/o/oauth2/auth',
						  request_token_url=None,
						  request_token_params={'scope': 'https://www.googleapis.com/auth/userinfo.profile',
												'response_type': 'code'},
						  access_token_url='https://accounts.google.com/o/oauth2/token',
						  access_token_method='POST',
						  access_token_params={'grant_type': 'authorization_code'},
						  consumer_key=GOOGLE_CLIENT_ID,
						  consumer_secret=GOOGLE_CLIENT_SECRET)

http_logger = urllib2.HTTPHandler(debuglevel = 1)
https_logger = urllib2.HTTPSHandler(debuglevel = 1)
opener = urllib2.build_opener(http_logger, https_logger)
urllib2.install_opener(opener)


@app.route('/')
def home():

	access_token = session.get('access_token')
	if access_token is None:
		return redirect(url_for('login'))
 
	access_token = access_token[0]
	
 
	headers = {'Authorization': 'OAuth '+access_token}
	request = urllib2.Request('https://www.googleapis.com/oauth2/v2/userinfo', None, headers)
	
	try:
		response = urllib2.urlopen(request)
		
	except urllib2.URLError, e:

		if e.code == 401:
			# Unauthorized - bad token
			session.pop('access_token', None)
			return redirect(url_for('login'))
		return response.read()
 
	return response.read()
 
 
@app.route('/login')
def login():

	callback=url_for('authorized', _external=True)
	return google.authorize(callback=callback)
 

@app.route(REDIRECT_URI)
@google.authorized_handler
def authorized(response):
	access_token = response['access_token']
	#print 'access token: {0}'.format(access_token)
	session['access_token'] = access_token, ''
	return redirect(url_for('home'))
 
 
@google.tokengetter
def get_access_token():
	return session.get('access_token')
 
 
def main():
	app.run()
 
 
if __name__ == '__main__':
		
	app.run(host='0.0.0.0', port=5000)

