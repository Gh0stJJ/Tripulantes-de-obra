from flask import Flask, render_template
from flask_login import LoginManager, UserMixin
from flask_sqlalchemy import SQLAlchemy
import os
from dotenv import load_dotenv
from werkzeug.security import generate_password_hash, check_password_hash
from flask_socketio import SocketIO
from models import User

#Templates folder
template_dir = os.path.abspath('../frontend')
static_dir = os.path.abspath('../frontend')

app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)
load_dotenv()
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')
app.config['UPLOAD_FOLDER'] = '../Frontend/static/uploads'
# app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
#csrf = CSRFProtect()
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
socketIO = SocketIO(app)



@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/', methods=['GET'])
def view_reviews():
    return render_template('index.html')

@app.route('/welcome', methods=['GET'])
def welcome():
    return render_template('welcome.html')


if __name__ == '__main__':
    #csrf.init_app(app)
    #app.run(debug=True,host='0.0.0.0', port=5000)
    socketIO.run(app,debug=True,host='0.0.0.0', port=5000)