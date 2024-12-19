from werkzeug.security import generate_password_hash, check_password_hash
from models import User, Profession, ProfessionalProfile
from extensions import db

# Crear un usuario con rol especificado
def create_user(full_name, national_id, phone, email, username, password, role='client'):
    if User.query.filter_by(email=email).first() or User.query.filter_by(username=username).first():
        return False, "El usuario o correo ya existe"

    hashed_password = generate_password_hash(password)
    new_user = User(
        full_name=full_name,
        national_id=national_id,
        phone=phone,
        email=email,
        username=username,
        password=hashed_password,
        role=role
    )
    db.session.add(new_user)
    db.session.commit()
    return True, "Usuario creado exitosamente"

# Buscar usuario por nombre de usuario
def find_user_by_username(username):
    return User.query.filter_by(username=username).first()

# Crear un trabajador profesional con perfil asociado
def create_professional(full_name, birth_date, national_id, phone, email, username, password, profession_name):
    # Verificar si usuario ya existe
    if User.query.filter_by(email=email).first() or User.query.filter_by(username=username).first():
        return False, "El usuario o correo ya existe"

    # Crear usuario con rol professional
    hashed_password = generate_password_hash(password)
    new_user = User(
        full_name=full_name,
        birth_date=birth_date,
        national_id=national_id,
        phone=phone,
        email=email,
        username=username,
        password=hashed_password,
        role='professional'
    )
    db.session.add(new_user)
    db.session.commit()

    # Buscar profesión
    profession = Profession.query.filter_by(name=profession_name.capitalize()).first()
    if not profession:
        db.session.rollback()
        return False, "Profesión no válida"

    # Crear perfil profesional asociado
    professional_profile = ProfessionalProfile(
        user_id=new_user.id,
        profession_id=profession.id
    )
    db.session.add(professional_profile)
    db.session.commit()

    return True, "Registro de trabajador exitoso"

# Verificar credenciales de inicio de sesión
def verify_user_credentials(username, password):
    user = find_user_by_username(username)
    if not user:
        return False, "Usuario no encontrado"
    if not check_password_hash(user.password, password):
        return False, "Contraseña incorrecta"
    return True, "Inicio de sesión exitoso"


def is_profile_incomplete(user_id):
    """
    Verifica si el perfil profesional de un usuario tiene campos importantes vacíos.
    """
    profile = ProfessionalProfile.query.filter_by(user_id=user_id).first()
    if not profile:
        return True  # No tiene perfil profesional, se considera incompleto

    # Verificar si alguno de los campos clave está vacío
    required_fields = [profile.location, profile.description, profile.phone]
    return any(field is None or field.strip() == "" for field in required_fields)

def update_professional_profile(user_id, description, location, phone, instagram, facebook, link):
    """
    Actualiza el perfil profesional de un usuario.
    """
    profile = ProfessionalProfile.query.filter_by(user_id=user_id).first()
    if not profile:
        return False, "Perfil profesional no encontrado"

    # Actualizar campos
    profile.description = description or profile.description
    profile.location = location or profile.location
    profile.phone = phone or profile.phone
    profile.instagram_link = instagram or profile.instagram_link
    profile.facebook_link = facebook or profile.facebook_link
    profile.extra_link = link or profile.extra_link

    db.session.commit()
    return True, "Perfil actualizado exitosamente"

# Consultar las profesiones desde la base de datos
def get_professions():
    return Profession.query.all()