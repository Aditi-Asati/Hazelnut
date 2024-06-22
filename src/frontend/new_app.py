import streamlit as st
import pyperclip  # This package is used to copy text to the clipboard

# Custom CSS to style the chat interface
st.markdown(
    """
    <style>
    .chat-container {
        border-radius: 15px;
        padding: 10px;
        margin: 10px 0;
        position: relative;
    }
    .chat-user {
        background-color: #FB6060;  /* Light red background for user text box */
        text-align: right;
        padding: 10px;
        border-radius: 15px;
        margin: 10px 0;
        color: #FFFFFF;
    }
    .chat-bot {
        background-color: #282EFC;
        padding: 10px;
        border-radius: 15px;
        margin: 10px 0;
        color: #FFFFFF;  /* Blue color for bot text */
        position: relative;
    }
    .copy-button {
        position: absolute;
        top: 10px;
        right: 10px;
        background-color: #1e90ff;
        color: #fff;
        border: none;
        padding: 5px 10px;
        border-radius: 5px;
        cursor: pointer;
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
    for i, chat in enumerate(st.session_state.chat_history):
        if chat["sender"] == "user":
            st.markdown(
                f'<div class="chat-container chat-user"><p>{chat["message"]}</p></div>',
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                f'<div class="chat-container chat-bot" id="bot-{i}"><p>{chat["message"]}</p></div>',
                unsafe_allow_html=True,
            )
            if "SELECT" in chat["message"]:
                # Add Copy Code button
                st.markdown(
                    f'<button class="copy-button" onclick="copyToClipboard(\'bot-{i}\')">Copy Code</button>',
                    unsafe_allow_html=True,
                )
                # Add question and Yes/No buttons
                st.write("Do you want to execute this query on your database?")
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("Yes", key=f"yes-{i}"):
                        st.write("Executing the query...")
                with col2:
                    if st.button("No", key=f"no-{i}"):
                        st.write("Query execution canceled.")

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

# JavaScript to copy text to clipboard
st.markdown(
    """
    <script>
    function copyToClipboard(containerid) {
        var range = document.createRange();
        range.selectNode(document.getElementById(containerid));
        window.getSelection().removeAllRanges(); 
        window.getSelection().addRange(range); 
        document.execCommand("copy");
        window.getSelection().removeAllRanges();
    }
    </script>
""",
    unsafe_allow_html=True,
)
