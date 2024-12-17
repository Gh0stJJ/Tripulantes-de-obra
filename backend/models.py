from extensions import db
from flask_login import UserMixin
from sqlalchemy import Column, Integer, String, Date, DateTime, ForeignKey, Enum, Table , Text
from sqlalchemy.orm import relationship
from datetime import datetime, timezone

SCHEMA = 'tripulantes' 

# Definición del tipo Enum para el rol del usuario
user_role_enum = Enum('client', 'professional', name='user_role')

# Tabla intermedia para la relación many-to-many entre Professions y Problems
profession_problems = Table(
    'profession_problems',
    db.metadata,
    db.Column('profession_id', db.Integer, db.ForeignKey(f'{SCHEMA}.professions.id', onupdate='CASCADE', ondelete='CASCADE'), primary_key=True),
    db.Column('problem_id', db.Integer, db.ForeignKey(f'{SCHEMA}.problems.id', onupdate='CASCADE', ondelete='CASCADE'), primary_key=True),
    schema=SCHEMA
)


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    __table_args__ = {'schema': SCHEMA} 

    id = Column(Integer, primary_key=True)
    full_name = Column(String(150), nullable=False)
    birth_date = Column(Date, nullable=False)
    national_id = Column(String(50))
    phone = Column(String(20))
    email = Column(String(150), nullable=False, unique=True)
    username = Column(String(50), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    role = Column(user_role_enum, nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    # Relación uno a uno con ProfessionalProfile
    professional_profile = relationship("ProfessionalProfile", uselist=False, back_populates="user")


class Profession(db.Model):
    __tablename__ = 'professions'
    __table_args__ = {'schema': SCHEMA} 

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False, unique=True)
    description = Column(Text)

    # Relación uno a muchos con ProfessionalProfile
    professionals = relationship("ProfessionalProfile", back_populates="profession")

    # Relación muchos a muchos con Problems
    problems = relationship("Problem", secondary=profession_problems, back_populates="professions")


class Problem(db.Model):
    __tablename__ = 'problems'
    __table_args__ = {'schema': SCHEMA} 

    id = Column(Integer, primary_key=True)
    description = Column(String(255), nullable=False)

    # Relación muchos a muchos con Professions
    professions = relationship("Profession", secondary=profession_problems, back_populates="problems")


class ProfessionalProfile(db.Model):
    __tablename__ = 'professional_profiles'
    __table_args__ = {'schema': SCHEMA}  # Esquema especificado

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey(f'{SCHEMA}.users.id', onupdate='CASCADE', ondelete='CASCADE'), nullable=False)
    profession_id = db.Column(db.Integer, db.ForeignKey(f'{SCHEMA}.professions.id', onupdate='CASCADE', ondelete='CASCADE'), nullable=False)
    location = db.Column(db.String(255))
    facebook_link = db.Column(db.String(255))
    instagram_link = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relaciones
    user = db.relationship("User", back_populates="professional_profile")
    profession = db.relationship("Profession", back_populates="professionals")
