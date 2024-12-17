from flask import Flask, render_template, request, jsonify
from flask_login import LoginManager
from dotenv import load_dotenv
from werkzeug.security import generate_password_hash , check_password_hash
from flask_socketio import SocketIO
import os

from extensions import db
from models import User
from database import create_user, find_user_by_username

#Templates folder
template_dir = os.path.abspath('../frontend')
static_dir = os.path.abspath('../frontend')

app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)
load_dotenv()
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')
app.config['UPLOAD_FOLDER'] = '../Frontend/static/uploads'
# app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
#csrf = CSRFProtect()
db.init_app(app)
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

@app.route('/login', methods=['GET'])
def login():
    return render_template('login.html')

@app.route('/register', methods=['POST'])
def register_user():
    try:
        data = request.get_json()
        full_name = data['full_name']
        birth_date = data['birth_date']
        national_id = data['national_id']
        phone = data['phone']
        email = data['email']
        username = data['username']
        password = data['password']

        success, message = create_user(full_name, birth_date, national_id, phone, email, username, password)
        if success:
            return jsonify({"message": message}), 200
        else:
            return jsonify({"message": message}), 400
    except Exception as e:
        return jsonify({"message": f"Error: {str(e)}"}), 500
    
@app.route('/register', methods=['GET'])
def register():
    return render_template('register.html')

@app.route('/problems', methods=['GET'])
def problems():
    return render_template('problems.html')

# Ruta para el inicio de sesión
@app.route('/login', methods=['POST'])
def login_user():
    try:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')

        # Buscar al usuario en la base de datos
        user = find_user_by_username(username)

        if not user:
            return jsonify({"message": "Usuario no encontrado"}), 404

        # Verificar la contraseña
        if not check_password_hash(user.password, password):
            return jsonify({"message": "Contraseña incorrecta"}), 401

        # Redirigir a problems.html
        return jsonify({"message": "Inicio de sesión exitoso"}), 200
    
    

    except Exception as e:
        return jsonify({"message": f"Error: {str(e)}"}), 500

if __name__ == '__main__':
    #csrf.init_app(app)
    #app.run(debug=True,host='0.0.0.0', port=5000)
    socketIO.run(app,debug=True,host='0.0.0.0', port=5000)