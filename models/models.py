from sqlalchemy import Boolean, Column, DateTime, Integer, String, Date, ForeignKey, func
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Task(Base):
    __tablename__ = 'tasks'
    id_tasks = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    description = Column(String)
    created_at = Column(DateTime, default=func.now())

class Rol(Base):
    __tablename__ = 'rol'
    id_rol = Column(Integer, primary_key=True, autoincrement=True)
    description = Column(String)

class User(Base):
    __tablename__ = 'users'
    id_user = Column(Integer, primary_key=True, autoincrement=True)
    fullName = Column(String)
    C_I = Column(Integer)
    bithdate = Column(Date)
    position = Column(String)
    status = Column(Boolean)
    created_at = Column(DateTime, default=func.now())
    id_rol = Column(Integer, ForeignKey('rol.id_rol', ondelete='CASCADE', onupdate='CASCADE')) 

    rol = relationship('Rol')

class Hour(Base):
    __tablename__ = 'hours'
    id_hours = Column(Integer, primary_key=True, autoincrement=True)
    hours = Column(Integer)
    date = Column(Date)
    description = Column(String)
    created_at = Column(DateTime, default=func.now())
    id_user = Column(Integer, ForeignKey('users.id_user', ondelete='CASCADE', onupdate='CASCADE'))
    id_tasks = Column(Integer, ForeignKey('tasks.id_tasks', ondelete='CASCADE', onupdate='CASCADE'))

    user = relationship('User')
    task = relationship('Task')