from fastapi import FastAPI
import uvicorn
from pydantic import BaseModel

from dotenv import load_dotenv
import os
import uuid

from src.query_builder.db_connector import DBConnector, DBConnectionError
from src.query_builder.query_executer import execute_query, QueryExecutionFailed
from src.query_builder.llm_integrator import ChatBot

load_dotenv()

uri = os.getenv("CONNECTION_STRING")

app = FastAPI()


class Item(BaseModel):
    host: str
    port: int
    username: str
    password: str
    database: str


@app.post("/submit")
async def form(item: Item):
    host = item.host
    port = item.port
    username = item.username
    password = item.password
    database = item.database
    dbconnector = DBConnector(host, username, password, int(port), database)
    try:
        dbconnector.connect_to_db()

    except Exception:
        raise DBConnectionError("Couldn't connect to the database, check credentials!")

    finally:
        session_id = str(uuid.uuid4())
        chatbot = ChatBot(dbconnector, session_id)
        chatbot.store_session_data()
        return {"session_id": session_id}


@app.post("/chat/{session_id}")
async def chat(session_id: str, question: str, item: Item):
    dbconnector = DBConnector(
        item.host, item.username, item.password, int(item.port), item.database
    )
    chatbot = ChatBot(dbconnector, session_id)
    answer = chatbot.generate_sql_query(question)
    return {"answer": answer}


@app.post("/execute")
def execute(item: Item, sql_query: str):
    dbconnector = DBConnector(
        item.host, item.username, item.password, int(item.port), item.database
    )
    result, columns = execute_query(sql_query, dbconnector)
    return {"result": result, "columns": columns}


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)
