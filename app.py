from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
from langchain_classic.agents import initialize_agent
from langchain_classic.agents.agent_types import AgentType
from dotenv import load_dotenv
from tools import increase_volume, open_application, open_folder,speak_text,text_to_speech_tool,browser_search,good_bye
from langchain_community.tools import DuckDuckGoSearchRun,Tool
from langchain_community.tools import WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper,OpenWeatherMapAPIWrapper
from langchain_google_community import GoogleSearchAPIWrapper
from stt import transcribe
import os

load_dotenv()
os.environ["OPENWEATHERMAP_API_KEY"] = os.getenv("OPENWEATHERMAP_API_KEY")
os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY")
groq_api_key = os.getenv("GROQ_API_KEY")
search_tool = DuckDuckGoSearchRun()
wikipedia_tool = WikipediaQueryRun(api_wrapper=WikipediaAPIWrapper())
weather = OpenWeatherMapAPIWrapper()
weather_tool = Tool(
    name="Weather",
    func=weather.run,
    description="Get current weather information for a given city"
)
search = GoogleSearchAPIWrapper(k=1)

Google_tool = Tool(
    name="google_search",
    description="Search Google for recent results.",
    func=search.run,
)
# prompt = ChatPromptTemplate.from_template("""
# You are a command normalizer for a Windows voice assistant.

# Your job:
# 1. Fix spelling mistakes
# 2. Remove filler words (um, uh, like, etc.)
# 3. Keep the command short and action-oriented
# 4. Return ONLY the refined command - no explanations

# Examples:
# - "umm can you like open chrome please" → "open chrome"
# - "increase the volum by 10" → "increase volume by 10"
# - "serch for weather in delhi" → "search for weather in delhi"

# Input command: {command}

# Refined command:
# """)

system_prompt = """
You are Wini, a fast and intelligent desktop AI assistant.

Your Goal: Execute the user's intent using the available tools.

Instructions:
1. **Ignore Noise:** The user input is transcribed speech. It may contain spelling errors (e.g., "paly music") or filler words ("um", "uh"). Ignore these and focus on the core intent.
2. **Direct Action:** If a tool exists for the request, USE IT immediately. Do not ask for confirmation.
3. **Reasoning:** If you need to search or use a tool, explain your thought process briefly in the 'Thought' step.
4. **Output:** Once the tool is used, give a concise final answer.
5. If you are usnure of anything and want some information to process further then politely ask user about the information and ask him to retry so that user can give you the command again
6. If a tool has already been used and the task is completed,
DO NOT call the tool again.
Return final answer immediately.
7. After final response is ready always make sure to use the speak_text tool at end for providing reply to user
Tools available: Google Search, Wikipedia, Weather, System Controls (Volume, Chrome) etc.
"""

# refiner_llm = ChatGroq(
#     model="llama-3.1-8b-instant",
#     groq_api_key=groq_api_key,
#     temperature=0
# )

agent_llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    groq_api_key=groq_api_key,
    temperature=0
)

# refine_chain = prompt | refiner_llm

# def refine_command(stt_text: str) -> str:
#     response = refine_chain.invoke({"command": stt_text})
#     return response.content.strip().lower()

def agent_call(command:str)->str:
    agent = initialize_agent(
    tools=[increase_volume,open_application, open_folder,search_tool,wikipedia_tool,speak_text,text_to_speech_tool,weather_tool,browser_search,good_bye],
    llm=agent_llm,
    system_message=system_prompt,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True,
    handle_parsing_errors = True,
    max_iterations=2
)
    if agent:
        result = agent.run(command)   
        return result

if __name__ == "__main__":
    raw = transcribe()
    print("🎤 Raw:", raw)

    refined = refine_command(raw)
    print("🧠 Refined:", refined)

    if refined:
        result = agent.run(refined)   
        print("🤖 Agent:", result)
    else:
        print("❌ Empty command")
