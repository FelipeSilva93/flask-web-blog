from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import click
from flask.cli import with_appcontext
from werkzeug.security import generate_password_hash
from .blog import blog_routes

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite+pysqlite:///flaskdb.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    CORS(app)

    db.init_app(app)

    app.register_blueprints(blog_routes.blogs)

    @click.command(name='create_admin')
    @with_appcontext
    def create_admin():
        admin = User(email='admin_email_address', password='admin_password')
        admin.password = generate_password_hash(admin.password,
                                                'sha256',
                                                salt_lenght=12)

        db.session.add(admin)
        db.session.commit()
        
    return app
