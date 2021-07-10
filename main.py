from flask import Flask, render_template
from flask_login import LoginManager

from models import db_session
from models.__all_models import *
from __all_routs import *
import sys
sys.path.append("..") # Adds higher directory to python modules path.



app = Flask(__name__)
app.config['SECRET_KEY'] = 'protected_secret_key'
app.config['PERMANENT_SESSION_LIFETIME'] = datetime.timedelta(days=365)
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    session = db_session.create_session()
    return session.query(User).get(user_id)


@app.route("/")
@app.route("/index")
def index():
    return render_template("index.html")


def main():
    db_session.global_init("db/tracks.sqlite")
    app.register_blueprint(auth_blueprint)
    app.register_blueprint(track_blueprint)
    app.register_blueprint(section_blueprint)
    app.register_blueprint(resource_blueprint)
    app.run()


if __name__ == '__main__':
    #app.run(port=8080, host='127.0.0.1')
    main()
