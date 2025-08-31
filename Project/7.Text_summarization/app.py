import validators, streamlit as st
from langchain.prompts import PromptTemplate
from langchain_groq import ChatGroq
from langchain.chains.summarize import load_summarize_chain
from langchain_community.document_loaders import YoutubeLoader, UnstructuredURLLoader
import os
from dotenv import load_dotenv

# Streamlit app setup
st.set_page_config(page_title="Langchain: Summarize Text from YouTube or Website", page_icon="🐦")
st.title("🐦 LangChain: Summarize Text From YT or Website")
st.subheader("Summarize URL")

# Load environment variables
load_dotenv()

# Sidebar API key input
with st.sidebar:
    groq_api_key = st.text_input("Groq_api_key", value="", type="password")

# URL input
url = st.text_input("URL ", label_visibility="collapsed")

# LLM setup
llm = ChatGroq(model="llama-3.3-70b-versatile", groq_api_key=groq_api_key)

# Prompt template
prompt_template = """
Provide a summary of the following content in 300 words:
content:{text}
"""
prompt = PromptTemplate(template=prompt_template, input_variables=['text'])

if st.button("Summarize the content from YT or Website"):
    if not groq_api_key.strip() or not url.strip():
        st.error("⚠️ Please provide both API key and URL.")
    elif not validators.url(url):
        st.error("⚠️ Please enter a valid URL (YouTube or website).")
    else:
        try:
            with st.spinner("Fetching transcript/content and summarizing..."):
                # Check if YouTube
                if "youtube.com" in url or "youtu.be" in url:
                    st.video(url)
                    loader = YoutubeLoader.from_youtube_url(url, add_video_info=True)
                else:
                    loader = UnstructuredURLLoader(
                        urls=[url],
                        ssl_verify=False,
                        headers={
                            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
                            "Accept-Language": "en-US"
                        }
                    )

                docs = loader.load()

                # Summarization chain
                chain = load_summarize_chain(llm, chain_type="stuff", prompt=prompt)
                summary = chain.run(docs)

                st.subheader("📝 Summary")
                st.success(summary)

        except Exception as e:
            st.error(f"❌ Exception: {e}")
