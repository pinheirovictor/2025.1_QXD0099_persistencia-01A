



import motor.motor_asyncio
import os
from dotenv import load_dotenv

load_dotenv()

client =  motor.motor_asyncio.AsyncIOMotorClient(
    os.getenv("MONGO_URL"))

database = client["escola"]

professores_collection = database["professores"]
alunos_collection = database["alunos"]
cursos_collection = database["cursos"]
turmas_collection = database["turmas"]
departamentos_collection = database["departamentos"]
matriculas__collection = database["matriculas"]