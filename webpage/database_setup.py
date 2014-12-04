import passwords

def add_config_params(app):
    app.config['MYSQL_DATABASE_USER'] = passwords.MYSQL_DATABASE_USER
    app.config['MYSQL_DATABASE_PASSWORD'] = passwords.MYSQL_DATABASE_PASSWORD
    app.config['MYSQL_DATABASE_DB'] = 'smarthouse'
    app.config['MYSQL_DATABASE_HOST'] = 'localhost'
