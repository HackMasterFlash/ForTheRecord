import os
from webapp import db, migrate, create_app
from webapp.media.models import Actor, Movie, Director


env = os.environ.get('WEBAPP_ENV', 'dev')
app = create_app('config.%sConfig' % env.capitalize())


@app.shell_context_processor
def make_shell_context():
    return dict(app=app, db=db, Actor=Actor, Movie=Movie, Director=Director, migrate=migrate)