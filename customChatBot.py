from langchain_groq import ChatGroq
from dotenv import load_dotenv
import streamlit as st
from streamlit_chat import message
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage

load_dotenv()

st.set_page_config(
    page_title = 'Your Custom ChatBot',
    page_icon = '🤖',
    #page_Layout = 'centered',
)

st.header('🤖 Your Custom ChatBot')

model = ChatGroq(model = 'llama-3.3-70b-versatile', temperature = 0.7)

if 'messages' not in st.session_state:
    st.session_state.messages = []

with st.sidebar:
    system_message = st.text_input('System Role', value='You are a helpful assistant.')
    user_prompt = st.text_input(label = 'Send a message')

    if system_message and not any (isinstance(msg, SystemMessage) for msg in st.session_state.messages):
        st.session_state.messages.insert(0, SystemMessage(content = system_message))
    
    if user_prompt:
        st.session_state.messages.append(
            HumanMessage(content = user_prompt)
        )

        with st.spinner('Generating response....'):
            response = model.invoke(
                st.session_state.messages
            )

            st.session_state.messages.append(
                AIMessage(content = response.content)
            )

if len(st.session_state.messages) >=1:
    if not isinstance(st.session_state.messages[0], SystemMessage):
        st.session_state.messages.insert(0, SystemMessage(content = 'You are a helpful assistant. '))

for i,msg in enumerate(st.session_state.messages[1:]):
    if i % 2 == 0:
        message(msg.content, is_user = True, key = f'{i} + 🤓')
    else:
        message(msg.content, is_user = False, key = f'{i} + 🤖')
