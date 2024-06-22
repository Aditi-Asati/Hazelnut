import streamlit as st

# Custom CSS to style the chat interface
st.markdown(
    """
    <style>
    .chat-container {
        border-radius: 15px;
        padding: 10px;
        margin: 10px 0;
    }
    .chat-user {
        background-color: #ffcccc;  /* Light red background for user text box */
        text-align: right;
        padding: 10px;
        border-radius: 15px;
        margin: 10px 0;
        color: #000;
    }
    .chat-bot {
        background-color: #e6f7ff;
        padding: 10px;
        border-radius: 15px;
        margin: 10px 0;
        color: #1e90ff;  /* Blue color for bot text */
    }
    .message-input {
        position: fixed;
        bottom: 0;
        width: 100%;
        background-color: #f9f9f9;
        padding: 10px;
        border-top: 1px solid #ccc;
    }
    .message-input input {
        width: 80%;
        padding: 10px;
        margin-right: 10px;
        border: 1px solid #ccc;
        border-radius: 5px;
    }
    .message-input button {
        padding: 10px 20px;
        border: none;
        border-radius: 5px;
        background-color: #1e90ff;
        color: #fff;
    }
    </style>
""",
    unsafe_allow_html=True,
)

# Initialize chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []


# Function to add messages to chat history
def add_message(sender, message):
    st.session_state.chat_history.append({"sender": sender, "message": message})


# Function to generate bot response (simple echo bot)
def generate_response(prompt):
    return f"Echo: {prompt}"


# Title of the app
st.title("Leena AI")

# Display the chat history
chat_container = st.container()
with chat_container:
    for chat in st.session_state.chat_history:
        if chat["sender"] == "user":
            st.markdown(
                f'<div class="chat-container chat-user"><p>{chat["message"]}</p></div>',
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                f'<div class="chat-container chat-bot"><p>{chat["message"]}</p></div>',
                unsafe_allow_html=True,
            )

# Placeholder for the input box to keep it at the bottom
input_placeholder = st.empty()

with input_placeholder.form(key="chat_form", clear_on_submit=True):
    user_input = st.text_input("Type your message here...", key="user_input")
    submit_button = st.form_submit_button(label="Send")

    if submit_button and user_input:
        # Add user message to chat history
        add_message("user", user_input)

        # Generate bot response
        bot_response = generate_response(user_input)

        # Add bot response to chat history
        add_message("bot", bot_response)

        # Refresh the page to update the chat history above the input box
        st.experimental_rerun()
