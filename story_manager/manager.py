from story_manager.connect_db import ConnectDatabase
from story_manager.models import Story, Status
from flask import Flask, request, session, g, redirect, url_for, abort, \
    render_template, flash, current_app

app = Flask(__name__)  # create the application instance :)
app.config.from_object(__name__)  # load config from this file , flaskr.py

# Load default config and override config from an environment variable
app.config.from_envvar('FLASKR_SETTINGS', silent=True)
app.secret_key = 'Some_secret'


def init_db():
    db = ConnectDatabase.db
    db.connect()
    db.drop_table(Story, fail_silently=True, cascade=True)
    db.drop_table(Status, fail_silently=True, cascade=True)
    db.create_tables([Status, Story], safe=True)


@app.cli.command('initdb')
def initdb_command():
    """Initializes the database."""
    init_db()
    Status.create_defaults()
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
    return render_template('create.html', story=Story.empty(), statuses=Status.select())


@app.route('/story', methods=['POST'])
def create_story():
    new_story = Story.create(title=request.form['title'],
                             user_story=request.form['user_story'],
                             acceptance_criteria=request.form['acceptance_criteria'],
                             business_value=request.form['business_value'],
                             estimation=request.form['estimation'],
                             status=request.form['status']
                             )
    new_story.save()
    flash('Story was successfully created')
    return redirect("/")


@app.route('/story/<story_id>', methods=['GET'])
def show_update_story_form(story_id):
    story = Story.select().where(Story.id == story_id).get()
    return render_template('update.html', story=story, statuses=Status.select())


@app.route('/story/<story_id>', methods=['POST'])
def update_story(story_id):
    Story.update(title=request.form['title'],
                 user_story=request.form['user_story'],
                 acceptance_criteria=request.form['acceptance_criteria'],
                 business_value=request.form['business_value'],
                 estimation=request.form['estimation'],
                 status=request.form['status'])\
        .where(Story.id == story_id).execute()
    flash('Story was successfully updated')
    return redirect("/")


@app.route('/story/delete/<story_id>', methods=['GET'])
def delete_story(story_id):
    Story.delete().where(Story.id == story_id).execute()
    flash('Story was successfully deleted')
    return redirect("/")
