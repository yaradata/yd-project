from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm import Session

from sqlalchemy.sql import func

from flask_bcrypt import Bcrypt
import logging as LOGGER
from models import Project
import requests

from werkzeug.security import generate_password_hash, check_password_hash

bcrypt = Bcrypt()

def create(session:Session, project:Project):
    try:
        existing_project = session.query(Project).filter(Project.name == project.name).first()
        if existing_project is None:
            session.add(project)  # Add the project
            session.commit()  # Commit the change 
            LOGGER.info(f"Created project: {project}")
        else:
            LOGGER.info(f"Users already exists in database: {existing_project}")
        return session.query(Project).filter(Project.name == project.name).first()
    except IntegrityError as e:
        LOGGER.error(e.orig)
        raise e.orig
    except SQLAlchemyError as e:
        LOGGER.error(f"Unexpected error when creating project: {e}")
        raise e 

def all(session:Session):
    try:
        projects = session.query(Project).all()
        return [ project for project in projects]
    except IntegrityError as e:
        LOGGER.error(e.orig)
        raise e.orig
    except SQLAlchemyError as e:
        LOGGER.error(f"Unexpected error when loging project: {e}")
        raise e 

def one(session:Session,project:dict):
    try:
        project = session.query(Project).filter(Project.id==project['id']).first() #.as_dict()
        print(project) 
        # .query.get(project['id']) #.first().as_dict()
        return project
    except Exception as e:
        LOGGER.error(f"error to get one project: {e}") 
        raise e 

def update(session:Session,project:dict):
    try:
        p = session.query(Project).filter(Project.id==project['id']).first() #.as_dict()
        p.name = project['name']
        p.updated_at = func.now() # project['updated_at']

        session.commit()

        return p 
    except Exception as e:
        LOGGER.error(f"error to get one project: {e}") 
        raise e 
     

def delete(session:Session,project:dict):
    try:
        project = session.query(Project).filter(Project.id==project['id']).delete() 
        return {'msg':'deleted'} 

    except IntegrityError as e:
        LOGGER.error(e.orig)
        raise e.orig
    except SQLAlchemyError as e:
        LOGGER.error(f"Unexpected error when loging project: {e}")
        raise e 



