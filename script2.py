import os
import streamlit as st
from langchain_community.utilities.sql_database import SQLDatabase
from langchain.chains import create_sql_query_chain
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.tools.sql_database.tool import QuerySQLDataBaseTool
from operator import itemgetter
from langchain_community.vectorstores import Chroma
from langchain_core.example_selectors import SemanticSimilarityExampleSelector
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate, ChatPromptTemplate, MessagesPlaceholder, FewShotChatMessagePromptTemplate
from langchain_core.runnables import RunnablePassthrough
from config import OPENAI_API_KEY, LANGCHAIN_API_KEY, LANGCHAIN_ENDPOINT, DB_URI
from langchain_chroma import Chroma

# Set up environment variables
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_ENDPOINT"] = LANGCHAIN_ENDPOINT
os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY
os.environ["LANGCHAIN_API_KEY"] = LANGCHAIN_API_KEY

db_uri = DB_URI
db = SQLDatabase.from_uri(db_uri)

# LLM setup
llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)

# Few-shot examples
examples = [
    {
        "input": "how many strains have an antibiotic type of AMP",
        "query": "SELECT COUNT(*) FROM amr_data WHERE antibiotic = 'AMP'"
    },
    {
        "input": "how many strains that have antibiotic type CAZ and resistance type S",
        "query": "SELECT COUNT(*) FROM amr_data WHERE antibiotic = 'CAZ' AND resistance = 'S'"
    },
    {
        "input": "how many strains are there in the database",
        "query": "SELECT COUNT(*) FROM strain_info"
    },
    {
        "input": "list all unique antibiotics in the database",
        "query": "SELECT DISTINCT antibiotic FROM amr_data"
    },
    {
        "input": "how many strains have resistance type R",
        "query": "SELECT COUNT(*) FROM amr_data WHERE resistance = 'R'"
    },
    {
        "input": "list all strains that are resistant to CIP",
        "query": "SELECT strain_id FROM amr_data WHERE antibiotic = 'CIP' AND resistance = 'R'"
    },
    {
        "input": "how many strains have a resistance type S for antibiotic GEN",
        "query": "SELECT COUNT(*) FROM amr_data WHERE antibiotic = 'GEN' AND resistance = 'S'"
    },
    {
        "input": "how many strains were collected in 2005",
        "query": "SELECT COUNT(*) FROM strain_info WHERE collection_year = 2005"
    },
    {
        "input": "list all distinct resistance types for antibiotic AMP",
        "query": "SELECT DISTINCT resistance FROM amr_data WHERE antibiotic = 'AMP'"
    },
    {
        "input": "list all strains with a resistance type of I for antibiotic TIG",
        "query": "SELECT strain_id FROM amr_data WHERE antibiotic = 'TIG' AND resistance = 'I'"
    },
    {
        "input": "how many strains have been tested with the antibiotic CAZ",
        "query": "SELECT COUNT(*) FROM amr_data WHERE antibiotic = 'CAZ'"
    },
    {
        "input": "how many strains have resistance type I",
        "query": "SELECT COUNT(*) FROM amr_data WHERE resistance = 'I'"
    },
    {
        "input": "how many distinct strains show susceptibility to GEN",
        "query": "SELECT COUNT(DISTINCT strain_id) FROM amr_data WHERE antibiotic = 'GEN' AND resistance = 'S'"
    },
    {
        "input": "list all strains that have been tested with antibiotic CIP",
        "query": "SELECT strain_id FROM amr_data WHERE antibiotic = 'CIP'"
    },
    {
        "input": "how many strains show resistance to CIP and were collected in 2006",
        "query": "SELECT COUNT(*) FROM amr_data ad INNER JOIN strain_info si ON ad.strain_id = si.strain_id WHERE ad.antibiotic = 'CIP' AND ad.resistance = 'R' AND si.isolation year = 2006"
    },
    {
        "input": "list all strains with antibiotic AMP and resistance type S",
        "query": "SELECT strain_id FROM amr_data WHERE antibiotic = 'AMP' AND resistance = 'S'"
    }
]


# Example prompt setup
example_prompt = ChatPromptTemplate.from_messages(
    [
        ("human", "{input}\nSQLQuery:"),
        ("ai", "{query}"),
    ]
)

# Semantic similarity selector setup
vectorstore = Chroma()
vectorstore.delete_collection()
example_selector = SemanticSimilarityExampleSelector.from_examples(
    examples,
    OpenAIEmbeddings(),
    vectorstore,
    k=16,  # Now we can use up to 3 examples
    input_keys=["input"],
)

few_shot_prompt = FewShotChatMessagePromptTemplate(
    example_prompt=example_prompt,
    example_selector=example_selector,
    input_variables=["input", "top_k"],
)

# Custom prompt template
final_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a MySQL expert. Given an input question, create a syntactically correct MySQL query to run. Unless otherwise specified.\n\nHere is the relevant table info: {table_info}\n\nBelow are a number of examples of questions and their corresponding SQL queries. These examples are just for reference and should be considered while answering follow-up questions."),
        few_shot_prompt,
        MessagesPlaceholder(variable_name="messages"),
        ("human", "{input}"),
    ]
)

# Get table information
table_info = db.table_info

# Generate query and execute query setup
generate_query = create_sql_query_chain(llm, db, final_prompt)
execute_query = QuerySQLDataBaseTool(db=db)

# Answer prompt
answer_prompt = PromptTemplate.from_template(
    """Given the following user question, corresponding SQL query, and SQL result, answer the user question.
    Question: {question}
    SQL Query: {query}
    SQL Result: {result}
    Answer: """
)

# Rephrase answer
rephrase_answer = answer_prompt | llm | StrOutputParser()

# Chain setup
chain = (
    RunnablePassthrough.assign(query=generate_query).assign(
        result=itemgetter("query") | execute_query
    )
    | rephrase_answer
)

# Function to process query
def process_query(question):
    response = chain.invoke({
        "question": question,
        "messages": st.session_state.messages,
        "table_info": table_info
    })
    return response

# Streamlit App
st.title("NL2SQL Chatbox")

# Initialize session state for chat history if it doesn't exist
if 'messages' not in st.session_state:
    st.session_state.messages = []

def send_message():
    user_message = f"You: {st.session_state.user_input}"
    st.session_state.messages.append(user_message)
    response = process_query(st.session_state.user_input)
    bot_message = f"Bot: {response}"
    st.session_state.messages.append(bot_message)
    st.experimental_rerun()  # Rerun the app to reset the input field

# Input field for user message
user_input = st.text_input("Type your message here:", key="user_input")

# Display chat history
st.write("Chat History:")
for message in st.session_state.messages:
    st.write(message)

# Button for sending message
if st.button("Send"):
    if st.session_state.user_input:
        send_message()
