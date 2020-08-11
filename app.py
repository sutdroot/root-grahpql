from flask import Flask
from flask_migrate import Migrate
from flask_graphql import GraphQLView
from flask_cors import CORS

from database import db_session, init_db, Base
from schema import schema

import json

app = Flask(__name__)
CORS(app)

with open('config.json') as f:
    config = json.load(f)

app.config.update(config)

migrate = Migrate(app, Base)

app.add_url_rule(
    '/graphql',
    view_func=(GraphQLView.as_view(
        'graphql',
        schema=schema,
        graphiql=True
    ))
)


@ app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()


if __name__ == "__main__":
    app.run()
