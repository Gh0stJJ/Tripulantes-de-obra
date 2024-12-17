from werkzeug.security import generate_password_hash
from models import User
from extensions import db



def create_user(full_name, birth_date, national_id, phone, email, username, password):
    if User.query.filter_by(email=email).first() or User.query.filter_by(username=username).first():
        return False, "Usuario o correo ya existe"

    hashed_password = generate_password_hash(password)
    new_user = User(
        full_name=full_name,
        birth_date=birth_date,
        national_id=national_id,
        phone=phone,
        email=email,
        username=username,
        password=hashed_password,
        role='client'  # Rol predeterminado
    )
    db.session.add(new_user)
    db.session.commit()
    return True, "Usuario creado exitosamente"

#busca al usuario en la base de datos
def find_user_by_username(username):
    return User.query.filter_by(username=username).first()