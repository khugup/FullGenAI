# RAG Q&A Conversation with 
import streamlit as st
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.chains import create_history_aware_retriever, create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.runnables.history import RunnableWithMessageHistory
from langchain_chroma import Chroma
from langchain_community.chat_message_histories import ChatMessageHistory, MessagePlaceholder
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.prompts import ChatPromptTemplate,MessagesPlaceholder
from langchain_groq import ChatGroq
from langchain_huggingface import HuggingFaceEmbeddings
import os
from dotenv import load_dotenv
load_dotenv()

os.environ['HF_TOKEN']=os.getenv("HF_TOKEN")
embeddings=HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

# Set up Streamlit
st.title("Conversational RAG with pdf uploads and chat history")
st.write("Upload PDF's and chat with their content ")

# Input the Groq API Key
api_key=st.text_input("Enter your GROQ API Key",type="password")

# Check if groq api key is provided
if api_key:
    llm=ChatGroq(groq_api_key=api_key,model_name='Gemma2-9b-It')
    
    # Chat interface
    sesion_id=st.text_input("Session ID",value="default_session")
    
    # statefully manage chat history
    if "store" not in st.session_state:
        st.session_state.store={}
    uploaded_files=st.file_uploader("Choose a PDF file",type="pdf",accept_multiple_files=True)    
    
    # process uploaded PDF's
    if uploaded_files:
        documents=[]
        for uploaded_file in uploaded_files:
            tempppdf=f"./temp.pdf"
            with open(tempppdf,"wb") as file:
                file.write(uploaded_file.getvalue())
                file_name=uploaded_file.name
            loader=PyPDFLoader(tempppdf)
            docs=loader.load()
        # Split and create embeddings for the documnets
        text_splitter=RecursiveCharacterTextSplitter(chunk_size=5000,chunk_overlap=500)
        splits=text_splitter.split_documents(documents)
        vectorstore=Chroma.from_documents(document=splits,embedding=embeddings)
        retriever=vectorstore.as_retriever()
        contextualize_q_system_prompt=(
            "Given a chat history and the latest user question"
            "which might reference context in the chat history,"
            "formulate a standalone question which can be understood"
            "without the chat history. Do not answr the question "
            "just reformulate it if needed and otherwise return it as is"
        )
        contextualize_q_prompt=ChatPromptTemplate.from_messages(
            [
                ("system",contextualize_q_system_prompt),
                MessagePlaceholder("chat_history"),
                ("human","{input}"),
            ]
        )
        history_aware_retriever=create_history_aware_retriever(llm,retriever,contextualize_q_prompt)
        
        # Answer question
        system_prompt=(
            "You are an assistant for question answering tasks. "
            "Use the following pieces of retrieved context to answer"
            "the question. If you don't know the answer, say thank you"
            "don't know. Use three sentences maximum nd keep the"
            "answer concise"
            "/n/n"
            "{context}"
        )
        qa_prompt=ChatPromptTemplate.from_messages(
            [
                ("system",contextualize_q_system_prompt),
                MessagePlaceholder("chat_history"),
                ("human","{input}"),
            ]
        )
        question_answer_chain=create_stuff_documents_chain(llm,qa_prompt)
        rag_chain=create_retrieval_chain(history_aware_retriever,question_answer_chain)
        session_id = "user1"
        def get_session_history(session_id:str)-> BaseChatMessageHistory:
            if session_id not in st.session_state.store:
                st.session_state.store[session_id]=ChatMessageHistory()
            return st.session_state.store[session_id]
        conversational_rag_chain=RunnableMessageHistory(
            rag_chain,get_session_history,
            input_messages_key="input",
            history_messages_key="chathistory",
            output_messages_key="answer"
        )
        user_input=st.text_input("Your question: ")
        if user_input:
            session_history=get_session_history(session_id)
            response=conversational_rag_chain.invoke(
                {"input":user_input},
                config={
                    "configurable":{"session_id":session_id}
                    
                },
            )
            st.write(st.session_state.store)
            st.sucess("Assistant: ",response['answer'])
            st.write("Chat History: ", session_history.messages)
else:
    st.warning("Please enetr the groq api key")
        
        
        
    
    
    
    
    
    