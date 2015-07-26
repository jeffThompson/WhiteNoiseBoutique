
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash
from contextlib import closing 			# for db connection


# the app itself!
app = Flask(__name__)

# load settings and override with environment var
app.config.update(dict(
	DATABASE = 		'/tmp/flaskr.db',
	USERNAME = 		'admin',
	PASSWORD = 		'default',
	SECRET_KEY = 	'development key',
	DEBUG = 		True
))
app.config.from_envvar('FLASKR_SETTINGS', silent=True)



# DATABASE FUNCTIONS

# connect to database
def connect_db():
	return sqlite3.connect(app.config['DATABASE'])

# initializes db
def init_db():
	with closing(connect_db()) as db:
		with app.open_resource('schema.sql', mode='r') as f:
			db.cursor().executescript(f.read())
		db.commit()

# function runs before a request is processed
# connection is stored in the special 'g' object from Flask
@app.before_request
def before_request():
	g.db = connect_db()

# after request
@app.teardown_request
def teardown_request(exception):
	db = getattr(g, 'db', None)
	if db is not None:
		db.close()


# VIEWS

# index page
# shows all entries in the db
# queries db and returns entries as tuples, which we
# then convert to dicts
# tuples are ordered as spec in the 'select' SQL statement
# then passes data to 'show_entries.html' template and gets rendered
@app.route('/')
def show_entries():
	cur = g.db.execute('select title, text from entries order by id desc')
	entries = [ dict(title=row[0], text=row[1]) for row in cur.fetchall() ]
	return render_template('show_entries.html', entries=entries)

# uploads post if logged in*
# only responds to POST requests and only if logged in
# if works, use 'flash()' to show message and go back to index
# * check if 'logged_in' key is present and == True
@app.route('/add', methods=['POST'])
def add_entry():
	if not session.get('logged_in'):
		abort(401)
	g.db.execute('insert into entries (title, text) values (?, ?)',
                 [request.form['title'], request.form['text']])
	g.db.commit()
	flash('New entry was successfully posted!')
	return redirect(url_for('show_entries'))

# login
# checks against username/pw hardcoded above
# also creates 'logged_in' key and sets it to True
# finally, successful login shows index page
# errors are sent back to the template
@app.route('/login', methods=['GET', 'POST'])
def login():
	error = None
	if request.method == 'POST':
		if request.form['username'] != app.config['USERNAME']:
			error = 'Invalid username'
		elif request.form['password'] != app.config['PASSWORD']:
			error = 'Invalid password'
		else:
			session['logged_in'] = True
			flash('You are now logged in!')
			return redirect(url_for('show_entries'))
	return render_template('login.html', error=error)

# logout
# removes key from the session
# pop() deletes key from dict if it exists, otherwise does nothing
# (keeps us from having to check if the user is logged in or not)
@app.route('/logout')
def logout():
	session.pop('logged_in', None)
	flash('You are now logged out!')
	return redirect(url_for('show_entries'))


# RUN IT
if __name__ == '__main__':
	app.run()










