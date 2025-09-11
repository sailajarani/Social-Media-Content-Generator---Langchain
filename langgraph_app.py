import os
from typing import TypedDict, List, Dict, Any
from dotenv import load_dotenv

load_dotenv()

from langgraph.graph import StateGraph, END
#from langchain_openai import ChatOpenAI
#from langchain_anthropic import ChatAnthropic
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.tools import DuckDuckGoSearchRun
from langchain.schema import HumanMessage, SystemMessage
from langchain.prompts import ChatPromptTemplate
from typing import TypedDict, Annotated

# Initialize models
linkedin_model = ChatOpenAI(
    model=os.environ.get("GOOGLE_GENAI_MODEL", "gemini-pro"),
    google_api_key=os.environ.get("GOOGLE_API_KEY")
)

instagram_model = ChatGoogleGenerativeAI(
    model=os.environ.get("GOOGLE_GENAI_MODEL", "gemini-pro"),
    api_key=os.environ.get("GOOGLE_API_KEY")
)

research_model = ChatGoogleGenerativeAI(
    model=os.environ.get("GOOGLE_GENAI_MODEL", "gemini-pro"),
    google_api_key=os.environ.get("GOOGLE_API_KEY")
)

# Initialize search tool
search_tool = DuckDuckGoSearchRun()

# Define the state structure
class SocialMediaState(TypedDict):
    topic: str
    research_summary: str
    linkedin_post: Annotated[str, "linkedin_agent"]
    instagram_reel_script: Annotated[str, "instagram_agent"]
    final_output: str

# Node functions
def research_node(state: SocialMediaState) -> SocialMediaState:
    """Research agent that researches the given topic"""
    topic = state["topic"]
    
    # Search for information
    search_results = search_tool.run(f"latest trends and information about {topic}")
    
    # Create research prompt
    research_prompt = ChatPromptTemplate.from_messages([
        SystemMessage(content="""
        You are a research assistant. You will be given a topic and search results. 
        Analyze the information and provide a comprehensive summary of the research.
        Focus on key insights, trends, and relevant information that can be used for social media content.
        """),
        HumanMessage(content=f"Topic: {topic}\n\nSearch Results: {search_results}")
    ])
    
    # Generate research summary
    response = research_model.invoke(research_prompt.format_messages())
    
    state["research_summary"] = response.content
    return state

def linkedin_agent_node(state: SocialMediaState) -> SocialMediaState:
    """LinkedIn post generator agent"""
    topic = state["topic"]
    research_summary = state["research_summary"]
    
    linkedin_prompt = ChatPromptTemplate.from_messages([
        SystemMessage(content="""
        You are a LinkedIn post generator. You will be given a topic with researched summary, and you will generate a LinkedIn post about it.
        The post should be professional, engaging, and relevant to the topic.
        
        Guidelines:
        - The post should have a primary hook, not more than 60 characters.
        - The post should have a line break after the hook.
        - The post should have a post-hook that is either supporting the hook or completely inverse of the hook to grab attention.
        - The post should be in a conversational tone and should be easy to read.
        - There should be bullet points in the post to make it easy to read.
        - There should be actionable items in the post to make it easy to follow.
        - At the end of the post, there should be a question to engage the audience.
        - Finally, ask the audience to share their thoughts in the comments. And to repost.
        - Use emojis to make the post more engaging.
        - Use hashtags to make the post more discoverable.
        """),
        HumanMessage(content=f"Topic: {topic}\n\nResearch Summary: {research_summary}")
    ])
    
    response = linkedin_model.invoke(linkedin_prompt.format_messages())
    state["linkedin_post"] = response.content
    return state

def instagram_agent_node(state: SocialMediaState) -> SocialMediaState:
    """Instagram reel script generator agent"""
    topic = state["topic"]
    research_summary = state["research_summary"]
    
    instagram_prompt = ChatPromptTemplate.from_messages([
        SystemMessage(content="""
        You are an Instagram reel script generator. You will be given a topic with researched summary, and you will generate a script for an Instagram reel about it.
        
        Guidelines:
        - The script should be engaging, fast paced, and relevant to the topic.
        - The script should have a primary hook, which grabs the attention of the audience.
        - The script should have a call to action at the end.
        - Format it as a script with timing and visual cues.
        """),
        HumanMessage(content=f"Topic: {topic}\n\nResearch Summary: {research_summary}")
    ])
    
    response = instagram_model.invoke(instagram_prompt.format_messages())
    state["instagram_reel_script"] = response.content
    return state

def posts_merger_node(state: SocialMediaState) -> SocialMediaState:
    """Merge the posts from LinkedIn and Instagram agents"""
    linkedin_post = state["linkedin_post"]
    instagram_script = state["instagram_reel_script"]
    
    merger_prompt = ChatPromptTemplate.from_messages([
        SystemMessage(content="""
        You are an AI Assistant responsible for combining linkedin and instagram reels script into a structured output.
        Your primary task is to merge the posts generated by the LinkedIn and Instagram agents into a single output. 
        Clearly mention the platform for each post and format them nicely.
        """),
        HumanMessage(content=f"LinkedIn Post: {linkedin_post}\n\nInstagram Reels Script: {instagram_script}")
    ])
    
    response = research_model.invoke(merger_prompt.format_messages())
    state["final_output"] = response.content
    return state

# Create the workflow graph
def create_social_media_workflow():
    """Create and return the LangGraph workflow"""

    # Create a new graph
    workflow = StateGraph(SocialMediaState)

    # Add nodes
    workflow.add_node("research", research_node)
    workflow.add_node("linkedin_agent", linkedin_agent_node)
    workflow.add_node("instagram_agent", instagram_agent_node)
    workflow.add_node("posts_merger", posts_merger_node)

    # Add edges - Sequential flow to avoid parallel update error
    workflow.set_entry_point("research")
    workflow.add_edge("research", "linkedin_agent")
    workflow.add_edge("linkedin_agent", "instagram_agent")
    workflow.add_edge("instagram_agent", "posts_merger")
    workflow.add_edge("posts_merger", END)

    # Compile the graph
    app = workflow.compile()
    return app

# Usage function
def generate_social_media_posts(topic: str) -> str:
    """Generate social media posts for a given topic"""
    
    # Create the workflow
    app = create_social_media_workflow()
    
    # Initial state
    initial_state = {
        "topic": topic,
        "research_summary": "",
        "linkedin_post": "",
        "instagram_reel_script": "",
        "final_output": ""
    }
    
    # Run the workflow
    final_state = app.invoke(initial_state)
    
    return final_state["final_output"]

# Example usage
if __name__ == "__main__":
    # Test the workflow
    topic = "AI in healthcare"
    result = generate_social_media_posts(topic)
    print("Generated Social Media Posts:")
    print("=" * 50)

    print(result)
