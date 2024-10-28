import os
from typing import List
from langchain.agents import create_structured_chat_agent, AgentExecutor
from langchain_google_genai import ChatGoogleGenerativeAI
from template import PROMPT_TEMPLATE
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
import streamlit as st

GOOGLE_API_KEY = st.secrets["GOOGLE_API_KEY"]

llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0, google_api_key=GOOGLE_API_KEY, convert_system_message_to_human=True)

def initialize_agent(tools: List, is_agent_verbose: bool = True, max_iterations: int = 5, return_thought_process: bool = True):
    prompt = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)

    memory = ChatMessageHistory(session_id="test-session")

    agent=create_structured_chat_agent(llm, tools, prompt)

    # Initialize agent
    agent_executor=AgentExecutor(agent=agent, tools=tools, verbose=is_agent_verbose, 
                                 handle_parsing_errors=True, max_iterations=max_iterations,
                                 return_intermediate_steps=return_thought_process
                                 )
    
    agent_with_chat_history = RunnableWithMessageHistory(
        agent_executor,
        # This is needed because in most real world scenarios, a session id is needed
        # It isn't really used here because we are using a simple in memory ChatMessageHistory
        lambda session_id: memory,
        input_messages_key="input",
        history_messages_key="chat_history",
    )

    return agent_with_chat_history
