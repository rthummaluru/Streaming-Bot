import streamlit as st
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI


load_dotenv()
st.set_page_config("Streaming Bot", page_icon=":books:")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

st.header("Streaming Bot")

#get response
def get_response(query, chat_history):
    template = f""""
    You are a helpful assistant, answer the following question given the history of the conversation

    History: {chat_history}

    Question: {query}
    """

    prompt = ChatPromptTemplate.from_template(template)

    llm = ChatOpenAI()

    chain = prompt | llm | StrOutputParser()

    return chain.stream({
        "chat_history": chat_history,
        "user_query": user_query
    })


#conversation
for message in st.session_state.chat_history:
    if isinstance(message, HumanMessage):
        with st.chat_message("Human"):
            st.markdown(message.content)
    else:
         with st.chat_message("AI"):
             st.markdown(message.content)

#user input
user_query = st.chat_input("Your Message")

if user_query is not None and user_query != "":
    st.session_state.chat_history.append(HumanMessage(user_query))
    
    with st.chat_message("Human"):
        st.markdown(user_query)

    with st.chat_message("AI"):
        ai_response = st.write_stream(get_response(user_query, st.session_state.chat_history))

    st.session_state.chat_history.append(AIMessage(ai_response))