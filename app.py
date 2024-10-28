import streamlit as st
from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.prompts import ChatPromptTemplate
import os
from langchain_groq import ChatGroq
import time
from langchain_core.output_parsers import StrOutputParser
from langchain_community.callbacks.streamlit import StreamlitCallbackHandler
import numpy as np
from PIL import Image, ImageColor
from util import get_colour_name

if "img_hair" not in st.session_state :
    st.session_state.img_hair = None  

if "agent" not in st.session_state :
    st.session_state.agent = None  

if "final_img" not in st.session_state :
    st.session_state.final_img = None  

if "hair_imgs_dict" not in st.session_state :
    st.session_state.hair_imgs_dict = {}

if "hair_imgs_generated_count" not in st.session_state :
    st.session_state.hair_imgs_generated_count = 0 

if "agent_results" not in st.session_state :
    st.session_state.agent_results = 0 

if "automatic_hair_root_area" not in st.session_state :
    st.session_state.automatic_hair_root_area = False

if "hex_color_name" not in st.session_state :
    st.session_state.hex_color_name = None

HUGGINGFACEHUB_API_TOKEN = st.secrets["HUGGINGFACEHUB_API_TOKEN"]
GROQ_API_KEY = st.secrets["GROQ_API_KEY"]
GOOGLE_API_KEY = st.secrets["GOOGLE_API_KEY"]

os.environ["HUGGINGFACEHUB_API_TOKEN"] = HUGGINGFACEHUB_API_TOKEN
os.environ["GROQ_API_KEY"] = GROQ_API_KEY

img_file = None

if "chat_history" not in st.session_state :
    st.session_state.chat_history = [AIMessage(content="Hello! I'm a Chatbot assistant. Ask me anything about your Web Page URL or PDF Files."),]

st.set_page_config(page_title="LangChain App", page_icon="🦜", layout="wide")

example_prompts = [
    "Hello how are you?",
    "What is your function?",
    "Tell me what you can do.",
    "Do you have a name?"
]

example_prompts_help = [
    "Example Message",
    "Example Message",
    "Example Message",
    "Example Message"
]

def get_agent_response(user_query) :
    #st_callback = StreamlitCallbackHandler(st.container())
    result = st.session_state.agent.invoke(
        {"input": user_query}, config={"configurable": {"session_id": "<foo>"}})
    result = result["output"]
    return result

def get_chatbot_simple_response(user_query, chat_history ) :
    template = """
    You are a helpful assistant. Answer the following questions considering the history of the conversation:

    Chat history: {chat_history}

    User question: {user_question}
    """

    prompt = ChatPromptTemplate.from_template(template)

    llm = ChatGroq(model="llama3-8b-8192", temperature=0.3, api_key=GROQ_API_KEY)

    chain = prompt | llm | StrOutputParser()
    
    return chain.invoke({
        "chat_history": chat_history,
        "user_question": user_query,
    })
    
def response_action(user_message) :
    st.session_state.chat_history.append(HumanMessage(content=user_message))
    with st.chat_message("user") :
        st.markdown(user_message)

    with st.chat_message("assistant") :
        ai_response = get_chatbot_simple_response(user_message, st.session_state.chat_history)
        message_placeholder = st.empty()
        full_response = ""
        # Simulate a streaming response with a slight delay
        for chunk in ai_response.split():
            full_response += chunk + " "
            time.sleep(0.05)

            # Add a blinking cursor to simulate typing
            message_placeholder.markdown(full_response + "▌")
        
        # Display the full response
        message_placeholder.info(full_response)

        st.session_state.chat_history.append(AIMessage(content=ai_response))

def get_agent_action(user_query) :
    st.session_state.chat_history.append(HumanMessage(content=user_query))
            
    with st.chat_message("user") :
        st.markdown(user_query)

    with st.chat_message("assistant") :
        with st.spinner("Generating Image 💇🏻...") :
            ai_response = get_agent_response(user_query)
            
        message_placeholder = st.empty()
        full_response = ""
        # Simulate a streaming response with a slight delay
        for chunk in ai_response.split():
            full_response += chunk + " "
            time.sleep(0.05)

            # Add a blinking cursor to simulate typing
            message_placeholder.markdown(full_response + "▌")
        
        # Display the full response
        message_placeholder.info(full_response)

        #if final_hair_img != None and ai_response == "Hair Modified Successfully!" :
        if ai_response == "Hair Modified Successfully!" :
            progress_bar = st.progress(0)

            for perc_completed in range(100) :
                time.sleep(0.001)
                progress_bar.progress(perc_completed+1)
                
            _,  col_img, _ = st.columns([0.85, 1, 0.85])
            col_img.image(st.session_state.final_img, use_column_width=True)
            #col_img.image(st.session_state.img_hair, use_column_width=True)
            col_img.button("Download Image", use_container_width=True, key=f"Button {str(st.session_state.hair_imgs_generated_count)}", icon="⏬")

            st.session_state.hair_imgs_dict[str(st.session_state.hair_imgs_generated_count)] = st.session_state.final_img
            st.session_state.hair_imgs_generated_count = st.session_state.hair_imgs_generated_count + 1


    st.session_state.chat_history.append(AIMessage(content=ai_response))
    
def main() :
    agent_results = 0
    _, col_1, _ = st.columns([1, 1, 1])
    
    col_1.image("./imgs/7.png")

    with st.expander("📚 How to Use this LangChain Application"):
        st.subheader("🦜 What is LangChain?")
        st.write("LangChain is a framework for developing applications powered by large language models (LLMs). LangChain serves as a generic interface for nearly any LLM, providing a centralized development environment to build LLM applications and integrate them with external data sources and software workflows.")
        st.write("LangChain’s module-based approach allows developers and data scientists to dynamically compare different prompts and even different foundation models with minimal need to rewrite code. This modular environment also allows for programs that use multiple LLMs. ")
        st.info("LangChain can facilitate most use cases for LLMs and natural language processing (NLP), like chatbots, intelligent search, question-answering, summarization services or even virtual agents capable of robotic process automation.")

        st.divider()

        st.subheader("🐍 RAG Application")
        st.write("Retrieval augmented generation, or RAG, is an architectural approach that can improve the efficacy of large language model (LLM) applications by leveraging custom data. This is done by retrieving data/documents relevant to a question or task and providing them as context for the LLM. RAG has shown success in support chatbots and Q&A systems that need to maintain up-to-date information or access domain-specific knowledge.")
        st.caption("RAG Diagram Representation:")
        _,  col_2, _ = st.columns([0.4, 1, 0.4])
        col_2.image("./imgs/rag-with-llms-1.gif", use_column_width=True)
        st.divider()

        st.markdown(
            """
            LangChain simplifies every stage of the LLM application lifecycle:
            
            - Development: Build your applications using LangChain's open-source building blocks, components, and third-party integrations. Use LangGraph to build stateful agents with first-class streaming and human-in-the-loop support.
            - Productionization: Use LangSmith to inspect, monitor and evaluate your chains, so that you can continuously optimize and deploy with confidence.
            - Deployment: Turn your LangGraph applications into production-ready APIs and Assistants with LangGraph Cloud.
            """
        )

        st.divider()

    st.divider()

    with st.sidebar:     
        st.info("**Start the RAG App ↓**", icon="👋🏾")
    
        with st.expander("🌐 Chatbot Application", expanded=True):
            st.title("🦜 Agent with LangChain")
            #st.divider()
            st.caption("📚 Load the Chatbot with PDFs, CSV or URL")
            #st.divider()
            st.success("RAG LangChain Chatbot with PDFs and URLs.")

            st.divider()

            st.write(
                """
                Load the Chatbot with PDFs, CSV or URL and Asks Questions About it. \n
                """
            )

            #st.success("RAG LangChain Chatbot with PDFs and URLs.")

            

            st.info("❗ It Can be Selected Only One Option at Time.")
            st.header("📍 Explore")
            option = st.multiselect("Options:", ["ReTouch", "Tutorial"], default=["ReTouch"], max_selections=1)

        if len(option) !=0 :
            option = option[0]

    st.caption("🚀 Powered by Llama-3, Gemini and LangChain")
    for index, message in enumerate(st.session_state.chat_history) :
        if isinstance(message, HumanMessage) :
            with st.chat_message("user") :
                st.markdown(message.content)
        else :
            with st.chat_message("assistant") :
                st.markdown(message.content)
                if len(st.session_state.hair_imgs_dict) !=  0 and message.content == "Hair Modified Successfully!" :
                    #for i in range(0, len(st.session_state.hair_imgs_list)) :
                    _,  col, _ = st.columns([0.85, 1, 0.85])
                    #col.image(final_hair_img, use_column_width=True, width=300)
                    #col.image(st.session_state.img_hair, width=300)

                    col.image(st.session_state.hair_imgs_dict[str(agent_results)], use_column_width=True)
                    col.button("Download Image", use_container_width=True, key=f"Button {str(agent_results)}", icon="⏬")

                    agent_results =  agent_results + 1


    #st.write(st.session_state.chat_history)


    button_cols = st.columns(4)

    user_query = ""

    if button_cols[0].button(example_prompts[0], help=example_prompts_help[0], key="Boton1", use_container_width=True, on_click=None):
        user_query = example_prompts[0]
        response_action(user_query)
    elif button_cols[1].button(example_prompts[1], help=example_prompts_help[1], key="Boton2", use_container_width=True, on_click=None):
        user_query = example_prompts[1]
        response_action(user_query)
    elif button_cols[2].button(example_prompts[2], help=example_prompts_help[2], key="Boton3", use_container_width=True, on_click=None):
        user_query = example_prompts[2]
        response_action(user_query)
    elif button_cols[3].button(example_prompts[3], help=example_prompts_help[3], key="Boton4", use_container_width=True, on_click=None):
        user_query = example_prompts[3]
        response_action(user_query)

    if option == "ReTouch" :
        with st.sidebar.expander("ReTouch Settings", icon="⚙️") :
            st.caption("Try this features for better results.")
            automatic_hair_root_area = st.checkbox("Automatic Selection of the Hair Root Area", value=True, help="Try this feature for better results.")
            st.warning("This option may or may not perform better in some images.")
            st.divider()
            col1, col2 = st.columns([1, 0.3], vertical_alignment="center", gap="medium")
            col1.info("Select a specific color code for the hair.")
            hex_code_color = col2.color_picker("Picker:")
            
            rgb_code_color = ImageColor.getcolor(hex_code_color, "RGB")
            actual_name, closest_name = get_colour_name(rgb_code_color)

            if (actual_name == None) :
                hair_color = (closest_name + '.')[:-1]
            elif (actual_name != None) :
                hair_color = (actual_name + '.')[:-1]

            st.session_state.automatic_hair_root_area = automatic_hair_root_area
            st.session_state.hex_color_name = hair_color


        with st.sidebar.expander("📚 RAG Option", expanded=True) :
            img_file = st.file_uploader("Upload PDF Files:", type=["jpg", "png", "jpeg"], accept_multiple_files=False)

        if img_file is None :
            st.divider()
            st.info("🖼️ Please Load an Image.")
        elif img_file is not None :
            image = np.array(Image.open(img_file))
            with st.sidebar.expander("🖼️ Image Preview:", expanded=True) :
                #st.success(" Image Loaded Correctly!", icon="✅")
                _,  img_preview, _ = st.columns([0.5, 1, 0.5])
                #col.image(final_hair_img, use_column_width=True, width=300)
                img_preview.image(image, use_column_width=True)
                #st.image(image, width=200)

            st.session_state.img_hair = img_file

            from ai_agent import initialize_agent
            from ai_tools import re_tools

            agent = initialize_agent(tools=re_tools)

            st.session_state.agent = agent 

            user_query = st.chat_input("Type your message here...")
            
            if user_query is not None and user_query != "":
                get_agent_action(user_query)

    elif option == "Conversation" :
        user_query = st.chat_input("Type your message here...")
            
        if user_query is not None and user_query != "":
            response_action(user_query)
        
if __name__ == "__main__" :
    main()
