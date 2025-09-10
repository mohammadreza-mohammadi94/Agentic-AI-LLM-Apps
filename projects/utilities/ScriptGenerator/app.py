#---------------------------------#
# Import Libraries and Setup App  #
#---------------------------------#

import streamlit as st
from langchain_cohere import ChatCohere
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain, SequentialChain
from langchain.memory import ConversationBufferMemory
from langchain.utilities import WikipediaAPIWrapper
import os
from dotenv import load_dotenv

# Setup API
load_dotenv()
COHERE_API_KEY = os.getenv("COHERE_API_KEY")
if not COHERE_API_KEY:
    raise ValueError("COHERE_API_KEY not found in .env file. Please set it.")
os.environ["COHERE_API_KEY"] = COHERE_API_KEY

#------------------------------#
# Implement App and Streamlit  #
#------------------------------#
st.title("Script Generator 🦜🔗")               # Set title for streamlit application

# Input
prompt = st.text_input("Write desired topic to generate script....")

# Prompt Templates
title_template = PromptTemplate(
    input_variables=['topic'],
    template = "Write me script title about {topic}"
)

script_template = PromptTemplate(
    input_variables=['topic', 'wikipedia_research'],
    template = 'write me script based on this TITLE :{title} while leveraging  this wikipedia research: {wikipedia_research}'
)

# Setup Memory
title_memory=ConversationBufferMemory(input_key='topic', memory_key='chat_history')
script_memory=ConversationBufferMemory(input_key='title', memory_key='chat_history')


# Setup LLMs
llm = ChatCohere(max_tokens=256, temperature=0.75)
title_chain=LLMChain(llm=llm,
                     prompt=title_template,
                     verbose=True, 
                     output_key='title', 
                     memory=title_memory)

script_chain=LLMChain(llm=llm, 
                      prompt=script_template, 
                      verbose=True, 
                      output_key='script', 
                      memory=script_memory)


#--------------------------#
# Setup Wikipedia Wrapper  #
#--------------------------#
wiki = WikipediaAPIWrapper()


# Run main application
if prompt:
    title = title_chain.run(prompt)
    wiki_research = wiki.run(prompt)
    script = script_chain.run(title=title, wikipedia_research=wiki_research)

    st.write(title)
    st.write(script)

    with st.expander('Title History'):
        st.info(title_memory.buffer)

    with st.expander('Script History'):
        st.info(script_memory.buffer)

    with st.expander('Wikipedia Research'):
        st.info(wiki_research)