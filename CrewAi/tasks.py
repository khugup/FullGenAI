from crewai import Task
from tools import yt_tool
from agents import blog_researcher, blog_writer

# Research Task
research_task = Task(
    description=(
        "Identify the video about {topic} and get detailed information "
        "from the channel including metadata, transcript, and insights."
    ),
    expected_output=(
        "A comprehensive 3-paragraph report based on the {topic} of the video content."
    ),
    tools=[yt_tool],   # YouTube channel search tool
    agent=blog_researcher,
)

# Writing Task
write_task = Task(
    description=(
        "Using the information gathered from the YouTube channel on the topic {topic}, "
        "create a detailed and engaging blog post."
    ),
    expected_output=(
        "A polished blog-style summary of the YouTube video content on {topic}."
    ),
    tools=[tool],   # your custom writing/summarization tool
    agent=blog_writer,
    async_execution=False,
    output_file="new-blog-post.md"  # ✅ correct param is singular
)
