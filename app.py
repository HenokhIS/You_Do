from flask import Flask
from config import Config
from models import db, User, Kegiatan, PersonalTask, Review, Catatan
from flask_login import LoginManager
from flask_jwt_extended import JWTManager
from flask_cors import CORS

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    db.init_app(app)
    
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'login'

    jwt = JWTManager(app) 

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    with app.app_context():
        db.create_all()
    
    from routes import routes as routes_blueprint
    app.register_blueprint(routes_blueprint)

    return app

from routes import *

app = create_app()

CORS(app, resources={r"/*": {"origins": "*"}})

if __name__ == '__main__':
    app.run(debug=True)
