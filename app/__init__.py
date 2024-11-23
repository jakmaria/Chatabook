from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from .models import db, bcrypt, User, Role, EventType  
from .routes import bp
from flask_migrate import Migrate

login_manager = LoginManager()
login_manager.login_view = 'main.login'
migrate = Migrate()

ROLE_TRANSLATIONS = {
    "Admin": {
        "name": "Správca",
        "rights": "Môžeš spravovať užívateľov, vytvárať, upravovať a mazať všetky rezervácie."
    },
    "User": {
        "name": "Užívateľ",
        "rights": "Môžeš vytvárať, upravovať a mazať svoje vlastné rezervácie."
    },
    "Guest": {
        "name": "Hosť",
        "rights": "Máš prístup len na prezeranie rezervácií."
    },
    "Visitor": {
        "name": "Návštevník",
        "rights": "Minimálny prístup. Môžeš sa prihlásiť, ale nemáš žiadne práva na rezervácie."
    }
}
#ChatGPT
def seed_data():
    # Seed roles
    roles = ["Admin", "User", "Guest", "Visitor"]
    for role_name in roles:
        if not Role.query.filter_by(name=role_name).first():
            db.session.add(Role(name=role_name))

    # Seed event types
    event_types = ["Oslava", "Posedenie s kamarátmi/známymi", "Ubytovanie pre priateľov/známych", "Iba rezervácia"]
    for event_name in event_types:
        if not EventType.query.filter_by(name=event_name).first():
            db.session.add(EventType(name=event_name))
    db.session.commit()

def create_app():
    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///chatabook.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'enigma'

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)

    @app.context_processor
    def inject_role_translations():
        return dict(role_translations=ROLE_TRANSLATIONS)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    with app.app_context():
        db.create_all()
        seed_data()
    
    app.register_blueprint(bp)
    
    return app