# NL2SQL

This projects consists of utilizing the OpenAI LLM, and a DB to find more insight about the information that lies in the DB.
The flow of the process goes as such:
Question -> LLM -> DB -> LLM ->answer
The code takes the human question, uses the LLM to turn it into a sql query with the knowledge of the DB properties, queries the answer and outputs the result back to the user.
