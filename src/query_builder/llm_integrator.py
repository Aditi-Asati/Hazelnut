from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage

from langchain_core.output_parsers import StrOutputParser
from langchain_community.llms import Ollama

from tabulate import tabulate
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv
import os
import pickle

from src.query_builder.db_connector import DBConnector
from src.query_builder.context_generator import DDLCommandGenerator
from src.query_builder.query_executer import execute_query


class ChatBot:

    def __init__(self, dbconnector: DBConnector, session_id) -> None:
        self.session_id = session_id
        self.context = DDLCommandGenerator(dbconnector).generate_ddl_command()
        self.llm = Ollama(model="llama3")
        self.output_parser = StrOutputParser()
        self.system_message = f""" ### Instructions:
        Your task is to convert a question into a SQL query, given a MySQL database schema.
        Adhere to these rules:
        - **Deliberately go through the question and MYSQL database schema word by word** to appropriately answer the question
        - When creating a ratio, always cast the numerator as float
        - You only need to provide the SQL query, without any other text
        - generated SQL query must end with semicolon ; and no other character like quotes etc
        - produce SQL query such that it can be directly executed on the given database
        - only respond to questions regarding the given database


        ### Input:
        Generate a SQL query that answers the given question.

        This query will run on a MYSQL database whose schema is given in this list: {self.context}


        """

        self.prompt_template = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    self.system_message,
                ),
                MessagesPlaceholder(variable_name="messages"),
            ]
        )
        self.chain = self.prompt_template | self.llm | self.output_parser
        # self.chat_history_list = []
        load_dotenv()
        uri = os.getenv("NEW_MONGODB_CONNECTION_STRING")
        self.client = MongoClient(uri, server_api=ServerApi("1"))
        self.db = self.client["Hazelnut"]
        self.collection = self.db["Hazelnut_chats"]

    def store_session_data(self):
        session_data = {
            "session_id": self.session_id,
            "chat_history_list": pickle.dumps([]),
        }
        self.collection.insert_one(session_data)

    def generate_sql_query(self, question: str):

        session_data = self.collection.find_one({"session_id": self.session_id})
        chat_history_list = pickle.loads(session_data["chat_history_list"])
        query = self.chain.invoke(
            {"messages": chat_history_list + [HumanMessage(content=question)]}
        )
        # query = self.chain.invoke(
        #     {"messages": self.chat_history_list + [HumanMessage(content=question)]}
        # )
        self.collection.update_one(
            {"session_id": self.session_id},
            {
                "$set": {
                    "chat_history_list": pickle.dumps(
                        chat_history_list
                        + [HumanMessage(content=question), AIMessage(content=query)]
                    )
                }
            },
        )
        # self.chat_history_list.append(HumanMessage(content=question))
        # self.chat_history_list.append(AIMessage(content=query))

        return query


if __name__ == "__main__":
    dbconnector = DBConnector(
        host="localhost", user="root", password="oursql", port=3306, database="pokedex"
    )

    chatbot = ChatBot(dbconnector)
    question1 = "provide names of pokemon which can mega evolve"
    question2 = "provide the sql query corresponding to the previous question"
    query = chatbot.generate_sql_query(question1)
    print("\nLLM output:\n", query, "\n")
    print("\nChat messages: ", chatbot.chat_history_list, "\n")
    query = chatbot.generate_sql_query(question2)
    print("\nLLM output:\n", query, "\n")
    print("\nChat messages: ", chatbot.chat_history_list, "\n")
    # result, columns = execute_query(query, dbconnector)
    # print(result)
    # table = tabulate(result, headers=columns, tablefmt="pretty")
    # print("\n\n", table)
