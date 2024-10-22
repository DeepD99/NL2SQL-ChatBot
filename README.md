# NL2SQL Chatbot & Palmona Pathogenomics AI Chatbot Project

## Table of Contents
1. [Getting Started](#getting-started)  
   - [Prerequisites](#prerequisites)  
   - [Installation](#installation)  
   - [Environment Variables Setup](#environment-variables-setup)  
   - [Running the Application](#running-the-application)  
   - [All Requirements for the Project](#sample-requirementstxt)  
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

Also make sure you have created accounts for OpenAI and LangChain, you must create an API key for both

- **OpenAi** (https://platform.openai.com/docs/quickstart/create-and-export-an-api-key)
- **LangChain** [(https://www.langchain.com/](https://docs.smith.langchain.com/how_to_guides/setup/create_account_api_key))

### Installation

1. **Clone the Repository**  
   Open your terminal and clone the repository:
   ```bash
   git clone <repository-url>
   cd <repository-folder>

2. **Install the requirements**
   Run this command:
   pip install -r requirements.txt

