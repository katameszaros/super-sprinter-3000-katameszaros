import os
from peewee import *
from story_manager.connect_db import ConnectDatabase
from story_manager.models import Story
from flask import Flask, request, session, g, redirect, url_for, abort, \
    render_template, flash, current_app


app = Flask(__name__)  # create the application instance :)
app.config.from_object(__name__)  # load config from this file , flaskr.py

# Load default config and override config from an environment variable
app.config.update(dict(

))
app.config.from_envvar('FLASKR_SETTINGS', silent=True)


def init_db():
    db = ConnectDatabase.db
    db.connect()
    db.create_tables([Story], safe=True)


@app.cli.command('initdb')
def initdb_command():
    """Initializes the database."""
    init_db()
    print('Initialized the database.')


@app.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the request."""
    if hasattr(g, 'postgre_db'):
        g.postgre_db.close()


@app.route('/')
def show_entries():
    entries = Story.select().order_by(Story.id.desc())
    return render_template('list.html', entries=entries)


@app.route('/story', methods=['POST'])
def add_entry():
    if not session.get('logged_in'):
        abort(401)
    new_entry = Story.create(title=request.form['title'],
                               text=request.form['text'])
    new_entry.save()
    flash('New entry was successfully posted')
    return redirect(url_for('show_entries'))


@app.route('/story/<story_id>', methods=['GET', 'POST'])
def login():
    print(app.config['USERNAME'])
    print(app.config['PASSWORD'])
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid username'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('show_entries'))
    return render_template('login.html', error=error)


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('show_entries'))


