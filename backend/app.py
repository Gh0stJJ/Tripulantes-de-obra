from flask import Flask, render_template, request, jsonify
from flask_login import LoginManager, current_user, login_user
from dotenv import load_dotenv
from werkzeug.security import generate_password_hash , check_password_hash
from flask_socketio import SocketIO
from problems_data import PROBLEMS_DATA
import os

from extensions import db
from models import User
from database import *

#Templates folder
template_dir = os.path.abspath('../frontend')
static_dir = os.path.abspath('../frontend')

app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)
load_dotenv()
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')
app.config['UPLOAD_FOLDER'] = '../Frontend/static/uploads'
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
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
    return render_template('problems.html', problems=PROBLEMS_DATA)


@app.route("/problems/<problem_id>")
def problem_detail(problem_id):
    problem = PROBLEMS_DATA.get(problem_id)
    if not problem:
        return "Problema no encontrado", 404
    return render_template("problem_detail.html", problem=problem)

# Ruta para el inicio de sesión
@app.route('/login', methods=['POST'])
def handle_login():
    try:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')

        # Buscar al usuario en la base de datos
        user = find_user_by_username(username)

        if not user:
            return jsonify({"message": "Usuario no encontrado"}), 404
        
        #Autenticar al usuario con Flask-Login
        login_user(user)

        # Verificar la contraseña
        if not check_password_hash(user.password, password):
            return jsonify({"message": "Contraseña incorrecta"}), 401

        # Redirigir a problems.html
        return jsonify({"message": "Inicio de sesión exitoso"}), 200
    
    

    except Exception as e:
        return jsonify({"message": f"Error: {str(e)}"}), 500
    

@app.route('/professionals/<profession>')
def show_professionals(profession):
    professionals = get_professionals_by_profession(profession)
    if not professionals:
        return "Profesión no encontrada", 404
    return render_template("searcher.html", profession=profession.title(), professionals=professionals)

# Sección de rutas para el trabajador

@app.route('/welcome_worker')
def welcome_worker():
    return render_template('welcome_worker.html')

@app.route('/register_worker', methods=['POST', 'GET'])
def register_worker():
    if request.method == 'POST':
        try:
            data = request.get_json()
            success, message = create_professional(
                data['full_name'],
                data['birth_date'],
                data['national_id'],
                data['phone'],
                data['email'],
                data['username'],
                data['password'],
                data['profession']
            )
            if success:
                return jsonify({"message": message}), 200
            else:
                return jsonify({"message": message}), 400
        except Exception as e:
            return jsonify({"message": f"Error: {str(e)}"}), 500
    return render_template('register_worker.html')

@app.route('/login_worker', methods=['POST', 'GET'])
def login_worker():
    if request.method == 'POST':
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

            # Verificar que el usuario sea un profesional
            if user.role != 'professional':
                return jsonify({"message": "No tienes permisos para acceder aquí"}), 403

            # Autenticar al usuario con Flask-Login
            login_user(user)

            # Comprobar si el perfil está completo
            if is_profile_incomplete(user.id):
                return jsonify({"redirect": "/profession_form"}), 200
            else:
                return jsonify({"redirect": "/professions_worker"}), 200
        except Exception as e:
            return jsonify({"message": f"Error: {str(e)}"}), 500
    return render_template('login_worker.html')


@app.route('/profession_form', methods=['GET', 'POST'])
def profession_form():
    if request.method == 'GET':
        # Comprobar si el usuario está autenticado
        if not current_user.is_authenticated:
            return jsonify({"message": "Usuario no autenticado"}), 401

        # Pasar el nombre de usuario al template
        return render_template('profession_form.html', username=current_user.username)

    if request.method == 'POST':
        try:
            # Obtener datos enviados por el cliente
            data = request.get_json()
            description = data.get("description")
            location = data.get("location")
            phone = data.get("phone")
            instagram = data.get("instagram")
            facebook = data.get("facebook")
            link = data.get("link")

            # Actualizar el perfil profesional
            success, message = update_professional_profile(
                current_user.id, description, location, phone, instagram, facebook, link
            )
            if success:
                return jsonify({"message": message}), 200
            else:
                return jsonify({"message": message}), 400

        except Exception as e:
            return jsonify({"message": f"Error: {str(e)}"}), 500
        

@app.route('/professions_worker', methods=['GET'])
def professions_worker():
    # Consultar las profesiones desde la base de datos
    professions = get_professions()

    # Pasar las profesiones al template
    return render_template('professions_worker.html', professions=professions)


if __name__ == '__main__':
    #csrf.init_app(app)
    #app.run(debug=True,host='0.0.0.0', port=5000)
    socketIO.run(app,debug=True,host='0.0.0.0', port=5000)