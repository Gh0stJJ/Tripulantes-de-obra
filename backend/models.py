from datetime import datetime, timezone
from flask_login import UserMixin
from sqlalchemy import (
    Column, Integer, String, Date, DateTime, Text,
    ForeignKey, Enum, Table
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship


Base = declarative_base()

# Definición del tipo Enum para el rol del usuario
user_role_enum = Enum('client', 'professional', name='user_role')

# Tabla intermedia para la relación many-to-many entre Professions y Problems
profession_problems = Table(
    'profession_problems',
    Base.metadata,
    Column('profession_id', Integer, ForeignKey('professions.id', onupdate='CASCADE', ondelete='CASCADE'), primary_key=True),
    Column('problem_id', Integer, ForeignKey('problems.id', onupdate='CASCADE', ondelete='CASCADE'), primary_key=True)
)


class User(Base, UserMixin):
    __tablename__ = 'users'

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


class Profession(Base):
    __tablename__ = 'professions'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False, unique=True)
    description = Column(Text)

    # Relación uno a muchos con ProfessionalProfile
    professionals = relationship("ProfessionalProfile", back_populates="profession")

    # Relación muchos a muchos con Problems
    problems = relationship("Problem", secondary=profession_problems, back_populates="professions")


class Problem(Base):
    __tablename__ = 'problems'

    id = Column(Integer, primary_key=True)
    description = Column(String(255), nullable=False)

    # Relación muchos a muchos con Professions
    professions = relationship("Profession", secondary=profession_problems, back_populates="problems")


class ProfessionalProfile(Base):
    __tablename__ = 'professional_profiles'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id', onupdate='CASCADE', ondelete='CASCADE'), nullable=False)
    profession_id = Column(Integer, ForeignKey('professions.id', onupdate='CASCADE', ondelete='CASCADE'), nullable=False)
    location = Column(String(255))
    facebook_link = Column(String(255))
    instagram_link = Column(String(255))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relaciones
    user = relationship("User", back_populates="professional_profile")
    profession = relationship("Profession", back_populates="professionals")
