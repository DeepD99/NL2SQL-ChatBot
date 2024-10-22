# NL2SQL Chatbot

## This projects consists of utilizing the OpenAI LLM, and a DB to find more insight about the information that lies in the DB.
## The flow of the process goes as such:
## Question -> LLM -> DB -> LLM ->answer
## The code takes the human question, uses the LLM to turn it into a sql query with the knowledge of the DB properties, queries the answer and outputs the result back to the user.
## Created the functionality to 'chat' with the LLM using streamlit.
## Sensitive data is hidden in a config file, variables were imported in.

## Here is an article from which I got the code: https://blog.futuresmart.ai/mastering-natural-language-to-sql-with-langchain-nl2sql
## There is also a video that goes into depth explaining everything: https://www.youtube.com/watch?v=fss6CrmQU2Y

## Environment Variables Setup: The code configures environment variables needed for LangChain and OpenAI API access. These variables include tracing, API keys, and endpoint configuration ## (LANGCHAIN_TRACING_V2, LANGCHAIN_ENDPOINT, OPENAI_API_KEY, LANGCHAIN_API_KEY).

## Database Initialization: Connects to a database using SQLAlchemy by setting the db_uri and initializing the SQLDatabase object to handle SQL queries.

## LLM Model Setup: Initializes a ChatOpenAI model (GPT-3.5 Turbo) for generating responses. The temperature is set to 0, ensuring deterministic output.

## Few-shot Examples: Defines a list of few-shot examples that map user input to corresponding SQL queries. These examples are used to guide the model in formulating correct SQL queries based on input questions.

## Prompt Template Construction: Uses ChatPromptTemplate to create a custom template for interaction. The system is instructed to generate MySQL queries, and it references example SQL questions and their corresponding answers.

## Semantic Similarity Selector: Implements a semantic similarity-based selector (SemanticSimilarityExampleSelector) to choose relevant examples from the vectorstore (Chroma) based on the user input, helping the model craft better responses.

## Streamlit App for Chat Interface: Uses Streamlit to create a simple web application that allows users to input queries, receive responses, and display the chat history. The app stores chat messages in the session state and reruns to update the conversation after each query.

# Palmona Pathogenomics AI Chatbot Project

## 1. Motivation
One of the main driving forces behind creating this project was to gain experience with AI-related technologies. As AI is shaping the future, acquiring working knowledge in this field is invaluable. Additionally, expanding skills in tech provides versatility and opens up new opportunities.

## 2. Purpose of the Project
This project was developed to assist Palmona Pathogenomics in building a preliminary AI chatbot. The chatbot will provide paid subscribers with actionable insights based on their individual data, enhancing their ability to analyze and address health-related issues.

## 3. Problem Statement
Palmona Pathogenomics focuses on combating emerging pathogen strains that pose risks to public health. This technology enables users to:
- Uncover relationships between data points.
- Detect anomalies.
- Identify patterns that help predict pathogen behavior and guide the development of targeted interventions.

## 4. Lessons Learned
Throughout the challenges of getting the project off the ground—troubleshooting code and resolving dependency issues—I learned the value of patience. Building a project of this scope isn't impossible, but it requires perseverance and the ability to step back and approach problems methodically. Patience is a skill that can only be cultivated through experience.

