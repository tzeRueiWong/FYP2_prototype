import streamlit as st

import google.generativeai as genai
from load_creds import load_creds

creds = load_creds()

genai.configure(credentials=creds)


model = genai.GenerativeModel(
  model_name="tunedModels/test-fine-tune-model-3",

  generation_config = genai.types.GenerationConfig(
    temperature=0.9,
    max_output_tokens=200,
  )
)


def gen_text(prompt):
    #prompt = "I have severe acne on my face, its been lasting for months, what should i do?"
    result = model.generate_content(prompt)

    output = ""

    if result.candidates[0].finish_reason.name == "MAX_TOKENS":
        temp = model.generate_content(prompt + " . Shorten the result.")

        if temp.candidates[0].finish_reason.name == "SAFETY":
            output = "Result blocked as it may be inappropriate. Please try again with a different input."
        else:
            output = temp.text

    elif result.candidates[0].finish_reason.name == "SAFETY":
        output = "Result blocked as it may be inappropriate. Please try again with a different input."

    else:
        output = result.text

    yield output



if 'user' not in st.session_state:
    st.session_state.user = ''


if st.session_state.user == '':
    st.warning("Please log in to continue")
    
else:
    st.title("Chatbot")

    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Accept user input
    if prompt := st.chat_input("ask anything"):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        # Display user message in chat message container
        with st.chat_message("user"):
            st.markdown(prompt)

        # Display assistant response in chat message container
        with st.chat_message("assistant"):
            #response = st.write_stream(response_generator())
            response = st.write_stream(gen_text(prompt))

        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": response})



