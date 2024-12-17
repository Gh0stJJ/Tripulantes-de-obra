from flask import Flask
from extensions import db
from sqlalchemy import text  # Importar text
from dotenv import load_dotenv
import os

# Cargar variables de entorno
load_dotenv()

# Crear la aplicación Flask
app = Flask(__name__)

# Configuración de la base de datos
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicializar la base de datos
db.init_app(app)

# Función para probar la conexión
def test_db_connection():
    try:
        with app.app_context():
            # Ejecutar una consulta simple usando text()
            result = db.session.execute(text("SELECT 1")).scalar()
            if result == 1:
                print("✅ Conexión exitosa a la base de datos.")
            else:
                print("⚠️ La consulta no devolvió el resultado esperado.")
    except Exception as e:
        print(f"❌ Error al conectar con la base de datos: {e}")

if __name__ == "__main__":
    test_db_connection()
