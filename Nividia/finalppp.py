import streamlit as st
import os
from langchain_nvidia_ai_endpoints import NVIDIAEmbeddings,ChatNVIDIA
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_core.output_parsers import StrOutputParser

from dotenv import load_dotenv
load_dotenv()

# Load the Nvidia API Key
os.environ['NVIDIA_API_KEY']=os.getenv('NVIDIA_API_KEY')
llm=ChatNVIDIA(model="meta/llama-3.3-70b-instruct")
# if "final_documents" not in st.session_state:
#     st.session_state["final_documents"] = []
def vector_embedding():
    if "vectors" not in st.session_state:
        st.session_state.embeddings = NVIDIAEmbeddings()
        st.session_state.loader = PyPDFDirectoryLoader("./us_census")
        st.session_state.docs = st.session_state.loader.load()
        
        if not st.session_state.docs:
            st.error("⚠️ No PDF documents found in ./us_census. Please add files and try again.")
            return

        st.write(f"Loaded {len(st.session_state.docs)} documents")

        st.session_state.text_splitter = RecursiveCharacterTextSplitter(chunk_size=700, chunk_overlap=50)
        st.session_state.final_documents = st.session_state.text_splitter.split_documents(
            st.session_state.docs[:30]
        )

        if not st.session_state.final_documents:
            st.error("⚠️ No text could be extracted from PDFs. Check file contents.")
            return

        st.session_state.vectors = FAISS.from_documents(
            st.session_state.final_documents,
            st.session_state.embeddings
        )
        
st.title("Nvidia NIM Demo")
prompt=ChatPromptTemplate.from_template(
    """
    Answer the questions based on the provided context only.
    Pleaseprovide the mot accurate response based oh the question
    Context:{context}
    Questions:{input}
    """
)

prompt1=st.text_input("Enter your question from documents")
if st.button("Document Embedding"):
    vector_embedding()
    st.write("FAISS Vector Store DB Is Ready Using NVIDIAEMBEDDING")
    
import time
if prompt1:
    document_chain=create_stuff_documents_chain(llm,prompt)
    retriever=st.session_state.vectors.as_retriever()
    retrieval_chain=create_retrieval_chain(retriever,document_chain)
    start=time.process_time()
    response=retrieval_chain.invoke({"input":prompt1})
    print("Response time:",time.process_time()-start)
    st.write(response['answer'])
    
    # With a streamlit expander
    with st.expander("Document Similarity Search"):
        # Find relevant chunks
        for i,doc in enumerate(response['context']):
            st.write(doc.page_content)
            st.write("--------------------")