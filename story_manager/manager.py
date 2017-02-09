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
def show_stories():
    stories = Story.select().order_by(Story.id.desc())
    return render_template('list.html', stories=stories)


@app.route('/story', methods=['GET'])
def show_create_story_form():
    return render_template('form.html', story=Story())


@app.route('/story', methods=['POST'])
def create_story():
    new_story = Story.create(title=request.form['storytitle']
                             # add all fields from form
                             )
    new_story.save()
    return redirect("/")


@app.route('/story/<story_id>', methods=['GET', 'POST'])
def edit_story(story_id):
    return render_template('form.html', story=Story(title="FAKE"))
