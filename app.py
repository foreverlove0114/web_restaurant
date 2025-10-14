import logging
import secrets
from flask import Flask, session
from flask_login import LoginManager

from online_restaurant_db import Session, Users
from config import AppConfig

from routes.auth_routes import auth_bp
from routes.profile_routes import profile_bp
from routes.menu_routes import menu_bp
from routes.order_routes import order_bp
from routes.main_routes import main_bp
from routes.admin_routes import admin_bp
from routes.reservations_routes import reservations_bp

app = Flask(__name__)

FILES_PATH = 'static/menu'

app.config['MAX_CONTENT_LENGTH'] = AppConfig.MAX_CONTENT_LENGTH
app.config['MAX_FORM_MEMORY_SIZE'] = AppConfig.MAX_FORM_MEMORY_SIZE
app.config['MAX_FORM_PARTS'] = AppConfig.MAX_FORM_PARTS

app.config['SESSION_COOKIE_SAMESITE'] = AppConfig.SESSION_COOKIE_SAMESITE

app.config['SECRET_KEY'] = AppConfig.SECRET_KEY

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.login'

log = logging.getLogger('werkzeug')
log.setLevel(logging.WARNING)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)  #

@login_manager.user_loader
def load_user(user_id):
    with Session() as session:
        user = session.query(Users).filter_by(id=user_id).first()
        if user:
            return user

@app.after_request
def apply_csp(response):
    nonce = secrets.token_urlsafe(16)
    csp = (
        f"default-src 'self'; "
        f"script-src 'self' 'nonce-{nonce}'; "
        f"style-src 'self'; "
        f"frame-ancestors 'none'; "
        f"base-uri 'self'; "
        f"form-action 'self'"
    )
    response.headers["Content-Security-Policy"] = csp
    response.set_cookie('nonce', nonce)
    return response

app.register_blueprint(main_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(profile_bp)
app.register_blueprint(menu_bp)
app.register_blueprint(order_bp)
app.register_blueprint(admin_bp)
app.register_blueprint(reservations_bp)

@app.before_request
def ensure_csrf():
    if "csrf_token" not in session:
        session["csrf_token"] = secrets.token_hex(16)

if __name__ == "__main__":
    app.run(port=8000, debug=False)
