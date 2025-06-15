"""Seed script to create base roles."""
import sqlalchemy as sa
from sqlalchemy.orm import Session
from app.models.auth import Base, Role
from sqlalchemy import create_engine

engine = create_engine('sqlite:///./test.db')

Base.metadata.create_all(engine)

roles = [
    {'slug': 'student', 'title': 'Student'},
    {'slug': 'parent', 'title': 'Parent'},
    {'slug': 'teacher', 'title': 'Teacher'},
    {'slug': 'manager', 'title': 'Manager'},
    {'slug': 'admin', 'title': 'Admin'},
]

with Session(engine) as session:
    for role in roles:
        exists = session.query(Role).filter_by(slug=role['slug']).first()
        if not exists:
            session.add(Role(**role))
    session.commit()
