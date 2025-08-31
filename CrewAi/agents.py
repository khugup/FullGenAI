from crewai import Agent
from tools import yt_tool
import os

# Environment variables for OpenAI
os.environ['OPENAI_API_KEY'] = os.getenv("OPENAI_API_KEY")
os.environ['OPENAI_MODEL_NAME'] = "gpt-4-0125-preview"

# Create a senior blog content researcher
blog_researcher = Agent(
    role='Blog Researcher from YouTube Videos',
    goal='Get the relevant video content for the topic {topic} from the YouTube channel',
    verbose=True,
    memory=True,
    backstory=(
        "Expert in understanding videos about AI, Data Science, Machine Learning, and Generative AI."
    ),
    tools=[yt_tool],
    allow_delegation=True
)

# Create a senior blog writer agent
blog_writer = Agent(
    role='Blog Writer',
    goal='Narrate compelling tech stories about the video {topic}',
    verbose=True,
    memory=True,
    backstory=(
        "With a flair for simplifying complex topics, you craft engaging narratives "
        "that captivate and educate, bringing new discoveries to light in an accessible manner."
    ),
    tools=[yt_tool],
    allow_delegation=False
)
