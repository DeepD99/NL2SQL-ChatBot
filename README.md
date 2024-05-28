# NL2SQL

## This projects consists of utilizing the OpenAI LLM, and a DB to find more insight about the information that lies in the DB.
## The flow of the process goes as such:
## Question -> LLM -> DB -> LLM ->answer
## The code takes the human question, uses the LLM to turn it into a sql query with the knowledge of the DB properties, queries the answer and outputs the result back to the user.

## Here is an article from which I got the code: https://blog.futuresmart.ai/mastering-natural-language-to-sql-with-langchain-nl2sql
## There is also a video that goes into depth explaining everything: https://www.youtube.com/watch?v=fss6CrmQU2Y
