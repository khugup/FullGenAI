from fastapi import FastAPI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_groq import ChatGroq
import os
from dotenv import load_dotenv
from langserve import add_routes

# Load environment variables
load_dotenv()
groq_api_key = os.getenv("GROQ_API_KEY")

# Make sure API key is set
if not groq_api_key:
    raise ValueError("❌ GROQ_API_KEY not found. Please set it in your .env file.")

# Correct model name
model = ChatGroq(model="gemma2-9b-it", groq_api_key=groq_api_key)

# 1. Create Prompt Template
generic_template = "Translate the following into {language}: "
prompt = ChatPromptTemplate.from_messages(
    [("system", generic_template), ("user", "{text}")]
)

# Output parser
parser = StrOutputParser()

# Create Chain
chain = prompt | model | parser

# App definition
app = FastAPI(
    title="Langchain Server",
    version="1.0",
    description="A simple API server using Langchain runnable interfaces"
)

# Add chain as an API route
add_routes(app, chain, path="/chain")

# Run server
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8000)
