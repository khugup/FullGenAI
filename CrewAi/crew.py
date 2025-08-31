# from crewai import Crew,Process
# from agents import blog_researcher,blog_writer
# from task import research_task,write_task

# # Forming the tech focused crew with some enhanced configuration
# crew=Crew(
#     agents=[blog_researcher,blog_writer],
#     tasks=[research_task,write_task],
#     process=Process,sequential,memory=True,
#     cache=True,
#     max_rpm=100,
#     share_crew=True,
# )

# # Start the task execution process with enhanced feedback
# result=crew.kickoff(inputs={"topic":"AI VS ML VS DL VS Data Science"})
# print(result)



from crewai import Crew, Process
from agents import blog_researcher, blog_writer
from tasks import research_task, write_task  # ✅ check your file name (tasks.py)

# Configure the crew process
crew = Crew(
    agents=[blog_researcher, blog_writer],
    tasks=[research_task, write_task],
    process=Process.sequential,   # ✅ correct usage
    cache=True,
    max_rpm=100,
    share_crew=True,
)

# Start the task execution
result = crew.kickoff(inputs={"topic": "AI VS ML VS DL VS Data Science"})

# Print the output
print(result)
