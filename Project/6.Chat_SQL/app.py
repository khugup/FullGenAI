import streamlit as st
from pathlib import Path
from langchain.agents import create_sql_agent
from langchain.sql_database import SQLDatabase
from langchain.agents.agent_types import AgentType
from langchain.callbacks import StreamlitCallbackHandler
from langchain.agents.agent_toolkits import SQLDatabaseToolkit
from sqlalchemy import create_engine
import sqlite3
from langchain_groq import ChatGroq
import os
from dotenv import load_dotenv

# Load .env variables
load_dotenv()

# Get the key
groq_api_key = os.getenv("GROQ_API_KEY")

st.set_page_config(page_title='Langchain: chat with sql db', page_icon="🐦")
st.title("🐦 Langchain: Chat with SQL DB")
INJECTION_WARNING="""
SQL agent can be vulnerable to prompt injection.Use a DB role with limited permission.
Read more [here](https://python.langchain.com/docs/security/).
"""

LOCALDB="USE_LOCALDB"
MYSQL="USE_MYSQL"
radio_opt=['Use SQLite 3 Database- Student.db',"Connect to you SQL Database"]
selected_opt=st.sidebar.radio(label="Choose the DB which you want to chat",options=radio_opt)
if radio_opt.index(selected_opt)==1:
    db_url=MYSQL
    my_sql_host=st.sidebar.text_input("Provide My SQL Host")
    my_sql_user=st.sidebar.text_input("MYSQL User")
    mysql_password=st.sidebar.text_input("MYSQL Password",type="password")
    msql_db=st.sidebar.text_input("My SQL Database")
else:
    db_url=LOCALDB
api_key=st.sidebar.text_input(label="GROQ API Key",type="password")

if not db_url:
    st.info("Please enter the database information and url")
    
# LLM Model
ChatGroq(groq_api_key=groq_api_key,model_name="Llama3-8b-8192",streaming=True)

@st.cache_resource(ttl="2g")
def configurable_db(db_uri,mysql_host=None,mysql_user=None,mysql_pssword=None,mysql_db=None):
    if db_url==LOCALDB:
        dffilepath=(Path(__file__).parent/"student.db")
        print(dffilepath)
        creator=lambda: sqlite3.connect(f"file:{dffilepath}?mode=ro",uri=True)
        return SQLDatabase(create_engine("sqlite:///",creator=creator))
    elif db_uri==MYSQL:
        if not (mysql_host and mysql_user and mysql_password and mysql_db):
            st.error("Please provide all MySQL connection details")
            st.stop()
            return SQLDatabase(create_engine(f"mysql+mysqlconnector://{my_sql_user}:{mysql_password}@{mysql_host}/{mysql_db}"))
        if db_uri==MYSQL:
            db=configurable_db(db_uri,mysql_host,mysql_user,mysql_password,mysql_db)
        else:
            db=configurable_db(db_uri)
            
            
# Toolkit
db = SQLDatabase.from_uri("sqlite:///student.db")
llm = ChatGroq(
    model="Gemma2-9b-It",   # or llama3-8b, mixtral-8x7b, etc.
    groq_api_key=os.getenv("GROQ_API_KEY")
)

toolkit=SQLDatabaseToolkit(db=db,llm=llm)
agent=create_sql_agent(
    llm=llm,
    toolkit=toolkit,
    verbose=True,
    agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION
)
if "messages" not in st.session_state or st.sidebar.button("Clear message history"):
    st.session_state["messages"]=[{"role":"assistant","content":"How can I help you?"}]
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])
user_query=st.chat_input(placeholder="Ask anything from the database")
if user_query:
    st.session_state.messages.append({"role":"user","content":user_query})
    st.chat_message("user").write(user_query)
    
    with st.chat_message("assistant"):
        streamlit_callback=StreamlitCallbackHandler(st.container())
        response=agent.run(user_query,callbacks=[streamlit_callback])
        st.session_state.messages.append({"role":"assistant","content":response})
        st.write(response)
    