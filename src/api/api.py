from fastapi import FastAPI
import uvicorn
from pydantic import BaseModel
from typing import Any

from query_builder.db_connector import DBConnector
from query_builder.query_executer import execute_query
from query_builder.llm_integrator import ChatBot

app = FastAPI()


class Item(BaseModel):
    data: dict[str, str]


dbconnector = DBConnector(
    host="localhost", user="root", password="oursql", port=3306, database="pokedex"
)
chatbot = ChatBot()


@app.get("/ping")
def ping():
    return "Hi! I am alive."


@app.post("/form")
async def form(item: Item):
    data = item.data
    host = data["host"]
    port = data["port"]
    username = data["username"]
    password = data["password"]
    database = data["database"]
    dbconnector = DBConnector(host, username, password, int(port), database)
    conn = dbconnector.connect_to_db()
    return conn
    #     return True
    # except Exception:
    #     raise DBConnectionError("Couldnt connect to the database, check credentials!")


@app.post("/predict")
async def predict(prompt: str):
    pass


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)
