# NL2SQL

## This projects consists of utilizing the OpenAI LLM, and a DB to find more insight about the information that lies in the DB.
## The flow of the process goes as such:
## Question -> LLM -> DB -> LLM ->answer
## The code takes the human question, uses the LLM to turn it into a sql query with the knowledge of the DB properties, queries the answer and outputs the result back to the user.
## Created the functionality to 'chat' with the LLM using streamlit.
## Sensitive data is hidden in a config file, variables were imported in.

## Here is an article from which I got the code: https://blog.futuresmart.ai/mastering-natural-language-to-sql-with-langchain-nl2sql
## There is also a video that goes into depth explaining everything: https://www.youtube.com/watch?v=fss6CrmQU2Y

## As you look into the code, one of the first things someone will see is the examples list.
## The examples list is meant to give the LLM an idea what the query should look based upon the input. It is essentially a guideline for the LLM to follow.
## Depending on what kind of schema is being used and the information within, the examples will look different, simply change them to fit your needs.
## Use this as an edge case scenario as well, if someone puts in something obscure, have an example closest to it to return an output.
## The example_prompt is for langchain and simply structures the inputs and outputs.
## Everything from line 104 to 130 is mainly setting up the few shot learning.
## After that the goal of the code is to setup the chain and execution of the queries, basically using builtin langchain functions to send the inputs over to langchain.
## The code after that is setting up the helper function for processing the chain executions, the streamlit aspect and dealing with the I/O of everything.

