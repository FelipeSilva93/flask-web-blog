from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import click
from flask.cli import with_appcontext
from werkzeug.security import generate_password_hash
from flask_jwt_extended import JWTManager

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite+pysqlite:///flaskdb.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY'] = '12345'
    CORS(app)
    db.init_app(app)
    jwt = JWTManager(app)

    from .blog import blog_routes
    app.register_blueprint(blog_routes.blogs)

    from user.user_model import User

    from login.login_route import login
    app.register_blueprint(login)

    @click.command(name='create_admin')
    @with_appcontext
    def create_admin():
        admin = User(email='admin_email_address', password='admin_password')
        admin.password = generate_password_hash(admin.password,
                                                'sha256',
                                                salt_lenght=12)

        db.session.add(admin)
        db.session.commit()

    app.cli.add_command(create_admin)
        
    return app
