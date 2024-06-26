import streamlit as st
from streamlit_chat import message
import requests
import pandas as pd
import pyperclip


FASTAPI_FORM_ENDPOINT = "http://localhost:8000/submit"
FASTAPI_CHAT_ENDPOINT = "http://localhost:8000/chat"
FASTAPI_EXECUTE_ENDPOINT = "http://localhost:8000/execute"

# Setting page title and header
st.set_page_config(page_title="AVA", page_icon=":robot_face:")
st.markdown(
    "<h1 style='text-align: center;'>Hazelnut- a helpful SQL chatbot </h1>",
    unsafe_allow_html=True,
)


# Initialise session state variables
if "generated" not in st.session_state:
    st.session_state["generated"] = []
if "past" not in st.session_state:
    st.session_state["past"] = []
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "system", "content": "You are a helpful assistant."}
    ]
if "session_id" not in st.session_state:
    st.session_state["session_id"] = []

# session_id = None
# Sidebar - let user choose model, show total cost of current conversation, and let user clear the current conversation
with st.sidebar:
    st.title("MYSQL server credentials")
    host = st.text_input("Enter the host:")
    port = st.text_input("Enter the port:")
    username = st.text_input("Enter your MYSQL username")
    password = st.text_input("Enter the password", type="password")
    database_name = st.text_input("Enter the database name you wish to connect to:")
    submit_form_button = st.sidebar.button("Submit")
    data = {
        "host": host,
        "port": port,
        "username": username,
        "password": password,
        "database": database_name,
    }
    # if submit_form_button(
    #     disabled=not (host and port and username and password and database_name)
    # ):
    if submit_form_button:
        data["port"] = int(data["port"])
        response = requests.post(url=FASTAPI_FORM_ENDPOINT, json=data)
        if response.status_code == 200:
            session_id = response.json()["session_id"]
            st.session_state["session_id"].append(session_id)
            # global session_id
            # st.warning("Please enter your credentials!", icon="⚠️")
            # else:
            st.success("Proceed to entering your prompt message!", icon="👉")

    clear_button = st.sidebar.button("Clear Conversation", key="clear")

# reset everything
if clear_button:
    st.session_state["generated"] = []
    st.session_state["past"] = []
    st.session_state["messages"] = [
        {"role": "system", "content": "You are a helpful assistant."}
    ]


# generate a response
def generate_response(prompt):
    st.session_state["messages"].append({"role": "user", "content": prompt})
    payload = {
        "question": prompt,
        "item": data,  # Convert the Pydantic model to a dictionary
    }
    response = requests.post(
        FASTAPI_CHAT_ENDPOINT + "/" + st.session_state["session_id"][-1], json=payload
    )
    # response = f"let me answer to the question {prompt}"
    st.session_state["messages"].append({"role": "assistant", "content": response})
    response.raise_for_status()
    if response.status_code == 200:
        answer = response.json()["answer"]
        return answer


# container for chat history
response_container = st.container()
# container for text box
container = st.container()

with container:
    with st.form(key="my_form", clear_on_submit=True):
        user_input = st.text_area("You:", key="input", height=100)
        submit_button = st.form_submit_button(label="Send")

    if submit_button and user_input:
        output = generate_response(user_input)
        st.session_state["past"].append(user_input)
        st.session_state["generated"].append(output)


if st.session_state["generated"]:
    with response_container:
        for i in range(len(st.session_state["generated"])):
            message(st.session_state["past"][i], is_user=True, key=str(i) + "_user")
            message(st.session_state["generated"][i], key=str(i))
            st.write("\t\tDo you want to execute this query on your database?")

            # Use columns for layout control
            col1, col2, col3 = st.columns(3)

            with col1:
                if st.button("Yes"):
                    st.write(f"Executing SQL query...")
                    payload = {
                        "query": st.session_state["generated"][i],
                        "item": data,  # Convert the Pydantic model to a dictionary
                    }
                    response = requests.post(FASTAPI_EXECUTE_ENDPOINT, json=payload)
                    response.raise_for_status()
                    if response.status_code == 200:
                        res = response.json()
                        result = res["result"]
                        columns = res["columns"]
                        table = pd.DataFrame(result, columns=columns)
                        st.dataframe(table)

            with col2:
                if st.button("No"):
                    pass
                    # st.write(f"No action taken ")

            with col3:
                if st.button("Copy query"):
                    pyperclip.copy(st.session_state["generated"][i])
