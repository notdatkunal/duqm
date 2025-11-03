from dotenv import load_dotenv,find_dotenv
import os

class __Config():
    def __init__(self,DB_NAME,DB_PASSWORD,DB_HOST,PORT,DB_USER):
        self.DB_NAME:str = DB_NAME
        self.DB_PASSWORD:str = DB_PASSWORD
        self.DB_HOST:str = DB_HOST
        self.PORT:str = PORT
        self.DB_USER:str = DB_USER 



def load_env_vars():
    load_dotenv(find_dotenv())
    env_vars = dict(os.environ)
    return __Config(
        DB_HOST= os.getenv("DB_HOST"),
        DB_NAME=os.getenv("DB_NAME"),
        DB_PASSWORD=os.getenv("DB_PASSWORD"),
        PORT=os.getenv("PORT"),
        DB_USER= os.getenv("DB_USER"),
    )

config = load_env_vars()