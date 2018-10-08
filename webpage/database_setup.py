import os

def add_config_params(app):
    app.config['MYSQL_DATABASE_USER'] = os.environ['MYSQL_DATABASE_USER']
    app.config['MYSQL_DATABASE_PASSWORD'] = os.environ['MYSQL_DATABASE_PASSWORD']
    app.config['MYSQL_DATABASE_DB'] = 'smarthouse'
    app.config['MYSQL_DATABASE_HOST'] = 'localhost'
