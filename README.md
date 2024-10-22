# NL2SQL Chatbot & Palmona Pathogenomics AI Chatbot Project

## Table of Contents
1. [Getting Started](#getting-started)  
   - [Prerequisites](#prerequisites)  
   - [Installation](#installation)
   - [Environment Variables Setup](#Environment-variables-setup)  
   - [Running the Application](#Running-the-application)  
   - [All Requirements for the Project](requirements.txt)  
2. [NL2SQL Chatbot Overview](#nl2sql-chatbot-overview)  
   - [Project Flow](#project-flow)  
   - [Functionality](#functionality)  
   - [References](#references)  
   - [Key Components](#key-components)  
     - [Environment Variables Setup](#environment-variables-setup-1)  
     - [Database Initialization](#database-initialization)  
     - [LLM Model Setup](#llm-model-setup)  
     - [Few-shot Examples](#few-shot-examples)  
     - [Prompt Template Construction](#prompt-template-construction)  
     - [Semantic Similarity Selector](#semantic-similarity-selector)  
     - [Streamlit Chat Interface](#streamlit-chat-interface)  
3. [Palmona Pathogenomics AI Chatbot Overview](#palmona-pathogenomics-ai-chatbot-overview)  
   - [Motivation](#motivation)  
   - [Purpose](#purpose)  
   - [Problem Statement](#problem-statement)  
   - [Lessons Learned](#lessons-learned)

---

## Getting Started

To get started with the NL2SQL Chatbot and Palmona Pathogenomics AI Chatbot Project, follow the steps below:

### Prerequisites

Make sure you have the following installed on your system:

- **Python** (version 3.8 or higher)
- **pip** (Python package manager)

Also make sure you have created accounts for OpenAI and LangChain, you must create an API key for both:

- **OpenAI** (https://platform.openai.com/docs/quickstart/create-and-export-an-api-key)
- **LangChain** [(https://www.langchain.com/](https://docs.smith.langchain.com/how_to_guides/setup/create_account_api_key))

### Installation

1. **Clone the Repository**  
   Open your terminal and clone the repository:
   ```bash
   git clone <repository-url>
   cd <repository-folder>

2. **Install the requirements**
   Run this command:
   ```bash
   pip install -r requirements.txt

### Environment-variables-setup

1. Before running the application, you need to set up the following environment variables. 
You can create a config.py file in the root directory of the project and add the following lines:

- LANGCHAIN_TRACING_V2=<your-tracing-value>
- LANGCHAIN_ENDPOINT=<your-endpoint-value>
- OPENAI_API_KEY=<your-openai-api-key>
- LANGCHAIN_API_KEY=<your-langchain-api-key>

Also have the DB your connecting to handy, as you will need the following information to put within the config file:

- USER = ""
- PASSWORD = ""
- HOST = ""
- PORT = ""
- DB = ""
- DB_URI = f"mysql+pymysql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DB}"

### Running-the-application

1. **Running the application**
   To run the project, go to the file titled 'Run', assign it the file extension .ipynb, this file will start streamlit and launch the chatbot

# NL2SQL Chatbot Overview

This project leverages the OpenAI LLM (Large Language Model) and a database (DB) to derive insights from the information stored within the database.

## Project Flow
The process follows this sequence:
- **Question** → **LLM** → **DB** → **LLM** → **Answer**

1. A human question is transformed by the LLM into a SQL query based on the database properties.
2. The query is executed on the database, retrieving the answer.
3. The LLM then returns the result to the user.

## Functionality
- Created a chat interface with Streamlit for user interaction with the LLM.
- Sensitive information (e.g., API keys) is stored in a config file, and relevant variables are imported into the code.

## References
- **Article:** [Mastering NL2SQL with LangChain](#) <https://blog.futuresmart.ai/mastering-natural-language-to-sql-with-langchain-nl2sql>
- **Video:** [YouTube Explanation](#) <https://www.youtube.com/watch?v=fss6CrmQU2Y>

## Key Components

### Environment Variables Setup
- Configures environment variables necessary for LangChain and OpenAI API.
- Includes: `LANGCHAIN_TRACING_V2`, `LANGCHAIN_ENDPOINT`, `OPENAI_API_KEY`, and `LANGCHAIN_API_KEY`.

### Database Initialization
- Connects to a database using SQLAlchemy by setting the `db_uri` and initializing a `SQLDatabase` object for handling SQL queries.

### LLM Model Setup
- Initializes a GPT-3.5 Turbo model via `ChatOpenAI`.
- Temperature is set to 0 to ensure deterministic responses.

### Few-shot Examples
- Defines several few-shot examples that map user inputs to SQL queries. These examples assist the LLM in crafting accurate SQL queries based on the given questions.

### Prompt Template Construction
- Uses `ChatPromptTemplate` to create a custom template.
- The model is instructed to generate MySQL queries using example questions and answers for reference.

### Semantic Similarity Selector
- Implements a `SemanticSimilarityExampleSelector` from the Chroma vectorstore.
- This selector identifies relevant examples to enhance the model’s performance by selecting the most similar examples based on the user’s input.

### Streamlit Chat Interface
- Uses Streamlit to build a simple web application for interaction.
- Stores chat history in the session state to maintain conversations across user inputs.


### Palmona Pathogenomics AI Chatbot Overview

## 1. Motivation
The primary motivation behind this project was to gain hands-on experience with AI-related technologies. As AI shapes the future, acquiring practical knowledge in this field is essential. Expanding skill sets across different areas of technology provides flexibility and opportunities for growth.

## 2. Purpose
The project was designed to help Palmona Pathogenomics build an AI-powered chatbot. This chatbot offers paid subscribers personalized insights by analyzing their individual data, enabling better decision-making in health-related scenarios.

## 3. Problem Statement
Palmona Pathogenomics focuses on combating emerging pathogen strains that threaten public health. The AI chatbot assists users by:
- Uncovering relationships between data points.
- Detecting anomalies in datasets.
- Identifying patterns to predict pathogen behavior and inform the development of targeted interventions.

## 4. Lessons Learned
Throughout the project, several challenges arose, including:
- Troubleshooting code and resolving dependency issues.
- Learning patience when results were not immediate.

This experience emphasized the importance of perseverance and the ability to take a step back when necessary. Patience is a critical skill, developed only through consistent practice and overcoming setbacks.


