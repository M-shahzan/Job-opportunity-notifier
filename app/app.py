from flask import Flask
from flask_login import LoginManager
from models import db, User
from config import Config
from routes import *
from flask import render_template
import os

app = Flask(__name__)
app.config.from_object(Config)

# Create upload directory
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

db.init_app(app)
login_manager = LoginManager(app)
login_manager.login_view = "auth.login"

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route("/")
def home():
    return render_template("home.html")

# Register blueprints
app.register_blueprint(auth_bp, url_prefix="/auth")
app.register_blueprint(seeker_bp, url_prefix="/seeker")
app.register_blueprint(employer_bp, url_prefix="/employer")

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
