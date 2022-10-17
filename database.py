from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os 


if os.environ.get("ENVIRONMENT") == "DEV": 
    engine = create_engine(
        'sqlite:///db.sqlite',
        # echo=True,
        connect_args={'check_same_thread': False}
    )
elif os.environ.get("ENVIRONMENT") == "PROD": 
    engine = create_engine(
        "postgresql://postgres:helloworld@database.capvm3mmwts6.us-east-1.rds.amazonaws.com:5432/circus",
        connect_args={'check_same_thread': False}
    )
else:
    raise "error to connect to database"


Session = sessionmaker(bind=engine)
session = Session() 


