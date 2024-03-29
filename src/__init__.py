from flask import Flask
from flask_login import LoginManager

from .models import db, generate_default_user



def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = 'secret-key-goes-here'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'

    db.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.init_app(app)

    from . import models
    with app.app_context():
      db.create_all()
      db.session.commit()
      generate_default_user()

    @login_manager.user_loader
    def load_user(user_id):
       return models.User.query.get(int(user_id))

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app