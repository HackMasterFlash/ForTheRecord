# The entry point for my Flask web app
# The app driver code for my ForTheRecord media consuming database interface
# This will nominally be a flask app


# To start I am going to follow the "Mastering Flask Web Development" by Daniel Gaspar example and use 
# the config.py file to set up the app

import os
from webapp import create_app

env = os.environ.get('WEBAPP_ENV', 'dev')
app = create_app('config.%sConfig' % env.capitalize())


if __name__ == "__main__":
    app.run()