# %%
import os
from langchain_community.utilities.sql_database import SQLDatabase
from config import OPENAI_API_KEY, LANGCHAIN_API_KEY, LANGCHAIN_ENDPOINT, DB_URI
# from langchain import LangSmithClient

os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY

os.environ["LANGCHAIN_TRACING_V2"]= "true"

os.environ["LANGCHAIN_ENDPOINT"] = LANGCHAIN_ENDPOINT

os.environ["LANGCHAIN_API_KEY"] = LANGCHAIN_API_KEY

db_uri = DB_URI
db= SQLDatabase.from_uri(db_uri)


print(db.dialect)
print(db.get_usable_table_names())
print(db.table_info)

# %%
from langchain.chains import create_sql_query_chain
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
generate_query = create_sql_query_chain(llm, db)    
query = generate_query.invoke({"question": "How many strains are located in New York"})
# what is price of `1968 Ford Mustang`
print(query)


# %%
from langchain_community.tools.sql_database.tool import QuerySQLDataBaseTool
execute_query = QuerySQLDataBaseTool(db=db)
execute_query.invoke(query)

# %%
from operator import itemgetter

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough

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

chain.invoke({"question": "How many strains are there"})


# %%
examples = [
    {
        "input": "List all strains that have resistance to AMP",
        "query": "SELECT * FROM amr_data WHERE antibiotic = 'AMP'"
    },
    {
        "input": "List the strain that has antibiotic type CAZ and resistance type S",
        "query": "SELECT * FROM amr_data WHERE antibiotic = 'CAZ' & resistance = 'S'"
    }
]


# %%
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder,FewShotChatMessagePromptTemplate, PromptTemplate
example_prompt = ChatPromptTemplate.from_messages(
    [
        ("human", "{input}\nSQLQuery:"),
        ("ai", "{query}"),
    ]
)
few_shot_prompt = FewShotChatMessagePromptTemplate(
    example_prompt=example_prompt,
    examples=examples,
    # input_variables=["input","top_k"],
    input_variables=["input"],
)
print(few_shot_prompt.format(input1="How many strains are there?"))


# %%
from langchain_community.vectorstores import Chroma
from langchain_core.example_selectors import SemanticSimilarityExampleSelector
from langchain_openai import OpenAIEmbeddings

vectorstore = Chroma()
vectorstore.delete_collection()
example_selector = SemanticSimilarityExampleSelector.from_examples(
    examples,
    OpenAIEmbeddings(),
    vectorstore,
    k=2,
    input_keys=["input"],
)
example_selector.select_examples({"input": "how many strains do we have?"})
few_shot_prompt = FewShotChatMessagePromptTemplate(
    example_prompt=example_prompt,
    example_selector=example_selector,
    input_variables=["input","top_k"],
)
print(few_shot_prompt.format(input="How many strains are there?"))


# %%
final_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a MySQL expert. Given an input question, create a syntactically correct MySQL query to run. Unless otherwise specificed.\n\nHere is the relevant table info: {table_info}\n\nBelow are a number of examples of questions and their corresponding SQL queries."),
        few_shot_prompt,
        ("human", "{input}"),
    ]
)
print(final_prompt.format(input="How many strains are there?",table_info="some table info"))
generate_query = create_sql_query_chain(llm, db,final_prompt)
chain = (
RunnablePassthrough.assign(query=generate_query).assign(
    result=itemgetter("query") | execute_query
)
| rephrase_answer
)
chain.invoke({"question": "How many strains are resistance to AMP"})


# %%
# table_details_prompt = f"""Return the names of ALL the SQL tables that MIGHT be relevant to the user question. \
# The tables are:

# # {table_details}

# Remember to include ALL POTENTIALLY RELEVANT tables, even if you're not sure that they're needed."""

# table_chain = create_extraction_chain_pydantic(Table, llm, system_message=table_details_prompt)
# tables = table_chain.invoke({"input": "give me details of resistance, antibiotic, and strain_id"})
# tables

# %%
chain = (
# RunnablePassthrough.assign(table_names_to_use=select_table) |
RunnablePassthrough.assign(query=generate_query).assign(
    result=itemgetter("query") | execute_query
)
| rephrase_answer
)
# which strain is antibiotic to AMP and has resistance to S?
# how many strains are antibiotic to AMP and has resistance to S?
# count how many antibiotics are AMP
chain.invoke({"question": "how many strains are susceptible to CAZ and from ny?"})

# %%
from langchain.memory import ChatMessageHistory
history = ChatMessageHistory()

# %%
final_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a MySQL expert. Given an input question, create a syntactically correct MySQL query to run. Unless otherwise specificed.\n\nHere is the relevant table info: {table_info}\n\nBelow are a number of examples of questions and their corresponding SQL queries. Those examples are just for referecne and hsould be considered while answering follow up questions"),
        few_shot_prompt,
        MessagesPlaceholder(variable_name="messages"),
        ("human", "{input}"),
    ]
)
print(final_prompt.format(input="How many strains are there?",table_info="some table info",messages=[]))


# %%
generate_query = create_sql_query_chain(llm, db,final_prompt)

chain = (
# RunnablePassthrough.assign(table_names_to_use=select_table) |
RunnablePassthrough.assign(query=generate_query).assign(
    result=itemgetter("query") | execute_query
)
| rephrase_answer
)

# %%
question = "How many strains with resistance to S are there"
response = chain.invoke({"question": question,"messages":history.messages})
# There are 2 customers with an order count of more than 5.


