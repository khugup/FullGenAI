import os
from dotenv import load_dotenv
from langchain_community.llms import Ollama
import streamlit as st
from langchain_core.output_parsers import StrOutputParser

from langchain_core.prompts import ChatPromptTemplate
load_dotenv()
# Langsmith Tracking
os.environ["LANGCHAIN_API_KEY"]=os.getenv("LANGCHAIN_API_KEY")
os.environ["LANGCHAIN_TRACKING_V2"]="true"
os.environ["LANGCHAIN_PROJECT"]=os.getenv("LANGCHAIN_PROJECT")


# Prompt Template
prompt=ChatPromptTemplate.from_messages(
    [
        ("system","You are a helpul assistant"),
        ("user","Question:{question}")
    ]
)
# Streamlit framework
st.title("Langchain Demo with llama2")
input_text=st.text_input("What question what you have in mind")

# Ollama Llama2 model
llm=Ollama(model="gemma:2b")
output_parser=StrOutputParser()
chain=prompt|llm|output_parser

if input_text:
    st.write(chain.invoke({"question":input_text}))
    