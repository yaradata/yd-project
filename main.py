# # from flask import Flask
from sqlalchemy.sql import func 

from database import session
from models import Project 
from orm import create as create_project
from orm import all as all_project
from orm import one as one_project
from orm import delete as delete_project 
from orm import update as update_project 

import uvicorn, os, logging
from fastapi import FastAPI, UploadFile, File, Response, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse

import pyfiglet

from logger import *

from pydantic import BaseModel

# from elasticapm.contrib.starlette import make_apm_client, ElasticAPM


"""
For PostgreSQL, use the following format:
postgresql://username:password@host:port/database_name

For MySQL:
mysql://username:password@host:port/database_name


User.query.filter_by(firstname='Sammy').all()
User.query.filter_by(id=3).first()

User.query.get(3)
User.query.get_or_404(User_id)

db.session.delete (model object)


## RelationShip
post1 = Post(title='Post The First', content='Content for the first post')
post2 = Post(title='Post The Second', content='Content for the Second post')
post3 = Post(title='Post The Third', content='Content for the third post')

comment1 = Comment(content='Comment for the first post', post=post1)
comment2 = Comment(content='Comment for the second post', post=post2)
comment3 = Comment(content='Another comment for the second post', post_id=2)
comment4 = Comment(content='Another comment for the first post', post_id=1)


db.session.add_all([post1, post2, post3])
db.session.add_all([comment1, comment2, comment3, comment4])

db.session.commit()
"""

"""
logging.debug('This is a debug message')
logging.info('This is an info message')
logging.warning('This is a warning message')
logging.error('This is an error message')
logging.critical('This is a critical message')
"""

# # os.chdir('/c/Users/user/Desktop/workspace/yara-datastorm/backend/apis/ml/')

app = FastAPI(
    title="AutoML",
    description="""**Project MS**""",
    version="0.0.1",
    contact={
        "name": "YaraData",
        "email": "yaradatateam@gmail.com",
    },
)


# db = SQLAlchemy() 


APP_PORT = os.environ.get("APP_PORT", default=8070)
APP_RELOAD = os.environ.get("APP_RELOAD", default=True)
APP_WORKERS = os.environ.get("APP_WORKERS", default=3)


# # elastic
# apm = make_apm_client(
# {
#     'SERVICE_NAME': '<SERVICE-NAME>',
#     'SECRET_TOKEN': '<SECRET-TOKEN>',
# })
# app = FastAPI()
# app.add_middleware(ElasticAPM, client=apm)
# # usage
# # apm.client.capture_exception()
# # apm.client.capture_message('hello, world!')



class ProjectNameUserIdModel(BaseModel):
    name: str
    user_id: int 

class ProjectIdModel(BaseModel):
    id: int 

class ProjectIdAndNameModel(BaseModel):
    id: int 
    name: str 



@app.get('/', response_class=RedirectResponse, include_in_schema=False)
async def docs():
    return RedirectResponse(url='/docs')


@app.get('/status')
def status():
    logger.info("{'status':'ok'}")
    return {'status':'ok'}


@app.post("/project/create")
def create(data:ProjectNameUserIdModel,response:Response):
    try:
        # print(type(data))
        # print(data.name)
        # project = Project(name="projet1",user_id=1) 
        project = Project(name=data.name,user_id=data.user_id) 
        create_project(session, project)
        logger.info(f"register {project}") 

        response.status_code = 201
        return {"msg": "project created"}
    except Exception as e: 
        logger.error(f"{e}") 
        response.status_code = 500
        return {'msg':f'{e}'} 
        

@app.get("/project/all")
def all(response:Response): 
    try:
        users = all_project(session)
        logger.info("get all user") 

        response.status_code = 200
        return {'result': users} 
    except Exception as e:
        logger.error(f"{e}") 
        return {'msg':f'error {e}'} 


@app.post("/project/one")
def one(data:ProjectIdModel, response:Response): 
    try:
        project_id = {'id':data.id} 
        user = one_project(session,project_id)
        # user = one_project(session, project_id)

        logger.info(f"login {user}") 
        response.status_code = 200
        return {'result': user} 
    except Exception as e:
        logger.error(f"{e}")
        response.status_code = 500
        return {'msg':f'error {e}'} 


@app.put("/project/update")
def update(data:ProjectIdAndNameModel, response:Response): 
    try:
        project = {'id':data.id,'name':data.name}
        user = update_project(session,project) 
        # user = one_project(session, project_id)  

        logger.info(f"login {user}") 
        response.status_code = 201
        return {'result': user} 
    except Exception as e:
        logger.error(f"{e}")
        response.status_code = 500
        return {'msg':f'error {e}'} 


@app.delete("/project/delete")
def delete(data:ProjectIdModel, response:Response): 
    try:
        project_id = {'id':data.id} 
        project = delete_project(session,project_id)

        logger.info(f"delete {project}") 
        return {'result': project} 
    except Exception as e:
        logger.error(f"{e}")
        response.status_code = 500
        return {'msg':f'error {e}'} 


if __name__ == "__main__":
    result = pyfiglet.figlet_format("Project MS")
    print(result)

    uvicorn.run("main:app", host="0.0.0.0", port=int(APP_PORT), reload=APP_RELOAD, workers=int(APP_WORKERS)) 
    

