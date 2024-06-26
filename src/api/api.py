from fastapi import FastAPI
import logging
import uvicorn
from pydantic import BaseModel

from dotenv import load_dotenv
import os
import uuid

from src.query_builder.db_connector import DBConnector, DBConnectionError
from src.query_builder.query_executer import execute_query, QueryExecutionFailed
from src.query_builder.llm_integrator import ChatBot

load_dotenv()

uri = os.getenv("NEW_MONGODB_CONNECTION_STRING")

app = FastAPI()


class DBCredentials(BaseModel):
    host: str
    port: int
    username: str
    password: str
    database: str


class ChatQuestion(BaseModel):
    question: str
    credentials: DBCredentials


@app.post("/submit")
def form(item: DBCredentials):
    host = item.host
    port = item.port
    print(port)
    username = item.username
    password = item.password
    database = item.database
    dbconnector = DBConnector(host, username, password, port, database)
    try:
        dbconnector.connect_to_db()

    except Exception as e:
        print(e)
        raise DBConnectionError("Couldn't connect to the database, check credentials!")

    session_id = str(uuid.uuid4())
    chatbot = ChatBot(dbconnector, session_id)
    chatbot.store_session_data()
    return {"session_id": session_id}


@app.post("/chat/{session_id}")
def chat(session_id: str, input: ChatQuestion):
    question = input.question
    credentials = input.credentials
    dbconnector = DBConnector(
        credentials.host,
        credentials.username,
        credentials.password,
        credentials.port,
        credentials.database,
    )
    chatbot = ChatBot(dbconnector, session_id)
    answer = chatbot.generate_sql_query(question)
    return {"answer": answer}


@app.post("/execute")
def execute(input: ChatQuestion):
    sql_query = input.question
    credentials = input.credentials
    dbconnector = DBConnector(
        credentials.host,
        credentials.username,
        credentials.password,
        credentials.port,
        credentials.database,
    )
    try:
        result, columns = execute_query(sql_query, dbconnector)
        return {"result": result, "columns": columns}
    except QueryExecutionFailed:
        return {"result": "unable to execute this query", "columns": []}
    except Exception as e:
        logging.exception(e)
        return {"result": "internal server error, please try again later", "columns": []}


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)
