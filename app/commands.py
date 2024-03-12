# from flask import Flask, current_app
from flask.cli import AppGroup
# from flask.cli import with_appcontext
from flask_migrate import Migrate, upgrade

deploy_cli = AppGroup('deploy')
migrate = Migrate()

@deploy_cli.command('db')
def deploy_db():
    from app import create_app, db
    app = create_app()
    with app.app_context():
        migrate.init_app(app, db)
        upgrade()
    print("Deploying database")