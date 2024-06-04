import os
import streamlit as st
from langchain_community.utilities.sql_database import SQLDatabase
from langchain.chains import create_sql_query_chain
from langchain_openai import ChatOpenAI
from langchain_community.tools.sql_database.tool import QuerySQLDataBaseTool
from operator import itemgetter
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from config import OPENAI_API_KEY, LANGCHAIN_API_KEY, LANGCHAIN_ENDPOINT, DB_URI

# Set up environment variables (use your own keys and endpoints)
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_ENDPOINT"] = LANGCHAIN_ENDPOINT
os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY
os.environ["LANGCHAIN_API_KEY"] = LANGCHAIN_API_KEY

db_uri = DB_URI
db = SQLDatabase.from_uri(db_uri)

llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
generate_query = create_sql_query_chain(llm, db)
execute_query = QuerySQLDataBaseTool(db=db)

# Function to process the NL2SQL query
def process_query(question):
    # query = generate_query.invoke({"question": question})
    # result = execute_query.invoke(query)
    answer_prompt = PromptTemplate.from_template(
        """Given the following user question, corresponding SQL query, and SQL result, answer the user question.
        Question: {question}
        SQL Query: {query}
        SQL Result: {result}
        Answer: """
    )
    rephrase_answer = answer_prompt | llm | StrOutputParser()
    chain = (
        RunnablePassthrough.assign(query=generate_query).assign(
            result=itemgetter("query") | execute_query
        )
        | rephrase_answer
    )
    response = chain.invoke({"question": question})
    return response  # Return the whole response, which will be handled later

# Streamlit App
st.title("NL2SQL Chatbox")

# Initialize session state for chat history if it doesn't exist
if 'messages' not in st.session_state:
    st.session_state.messages = []

# Function to send a message
def send_message():
    if st.session_state.user_input:
        user_message = f"You: {st.session_state.user_input}"
        st.session_state.messages.append(user_message)
        response = process_query(st.session_state.user_input)
        bot_message = f"Bot: {response}"
        st.session_state.messages.append(bot_message)
        st.session_state.user_input = ""  # Clear input field

# Input field for user message
user_input = st.text_input("Type your message here:", key="user_input", on_change=send_message)

# Display chat history
st.write("Chat History:")
for message in st.session_state.messages:
    st.write(message)

# To keep the chat box and messages in sync, use a button for sending messages
if st.button("Send"):
    send_message()
