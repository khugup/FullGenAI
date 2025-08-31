import streamlit as st
from langchain_groq import ChatGroq
from langchain.chains import LLMChain
from langchain.chains.llm_math.base import LLMMathChain
from langchain.prompts import PromptTemplate
from langchain_community.utilities import WikipediaAPIWrapper
from langchain.agents.agent_types import AgentType
from langchain.agents import Tool,initialize_agent
from dotenv import load_dotenv
from langchain.callbacks import StreamlitCallbackHandler
from langchain.chains import LLMMathChain


# Set up the streamlit app
st.set_page_config(page_title="Text to MATH Problem Solver and Data Search and Assistant",page_icon="🐦")
st.title("Text To Math Problem Solver Using Google Gemma2")
groq_api_key=st.sidebar.text_input(label="Groq API Key",type="password")


if not groq_api_key:
    st.info("Please add your Groq API Key to continue")
    st.stop()
    
    
llm=ChatGroq(model="gemma2-9b-it",groq_api_key=groq_api_key)

# Initializing the tools
wikipedia_wrapper=WikipediaAPIWrapper()
wikipedia_tool=Tool(
    name="Wikipedia",
    func=wikipedia_wrapper.run,
    description="A tool for searching the Internet to find the various information on the topic given"
    
)


# Initialize the MATH Tool
math_chain=LLMMathChain.from_llm(llm=llm)
calculator=Tool(
    name="Calculator",
    func=math_chain.run,
    description="A tool for answering math related questions. Only input mathematical expression need to be provided"
    
)
prompt="""
You are a agent tasked for solving users mathematical question.Logically arrive at the solution and provide detail explanation and display it point wise for the question below
Question:{question}
Answer:
"""
prompt_template=PromptTemplate(
    input_variables=['question'],
    template=prompt
)


# combine all the tools into chain
chain=LLMChain(llm=llm,prompt=prompt_template)

reasoning_tool=Tool(
    name="Reasoning_Tool",
    func=chain.run,
    description="A tool for answering logic based and reasoning questions"
    
)
# Initialize the agents
assistant_agent=initialize_agent(
    tools=[wikipedia_tool,calculator,reasoning_tool],
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=False,
    handle_parsing_error=True
)
if "messages" not in st.session_state:
    st.session_state['messages']=[
        {"role":"assistant","content":"Hi,Iam a Math Chaatbot who can answer all your maths problem"}
        
    ]
for msg in st.session_state.messages:
    st.chat_message(msg['role']).write(msg['content'])
    
# Function to generate the response
def generate_response(question):
    response=assistant_agent.invoke({"input":question})
    return response

# Lets start the interaction
# question=st.text_area("Two cities X and Y are 45 km apart. Two cars start from X and Y in the same direction with speeds of 30 km/hr and 15 km/hr, respectively. Both cars meet at point Z beyond Y. Find the distance ZY.")
question = """Two cities X and Y are 45 km apart. 
Two cars start from X and Y in the same direction with speeds of 30 km/hr and 15 km/hr, respectively. 
Both cars meet at point Z beyond Y. 
Find the distance ZY."""
user_input = st.text_area("Math Question", value=question, height=150)

st.write("You entered:")
st.write(user_input)

if st.button("find my answer"):
    if question:
        with st.spinner("Generate Response.."):
            st.session_state.messages.append({"role":"user","content":{question}})
            st.chat_message("user").write(question)
            st_cb=StreamlitCallbackHandler(st.container(),expand_new_thoughts=False)
            response=assistant_agent.run(st.session_state.messages,callbacks=[st_cb])
            st.session_state.messages.append({"role":"assistant","content":response})
            st.write("### Response")
            st.success(response)
    else:
        st.warning("Please enter the question")