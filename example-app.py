from openai import OpenAI
import streamlit as st
import os 

st.title("💬 Example Chatbot")
st.caption("🚀 A Streamlit chatbot powered by OpenAI")

# get API key from environment variable 
openai_api_key = os.environ['OPENAI_API_KEY']

with st.sidebar:
    # alternative: ask user for the API key 
    # openai_api_key = st.text_input("OpenAI API Key", key="openai_api_key", type="password")

    model_name = st.sidebar.selectbox(
       'Choose AI text model to use',
       ['gpt-4o-mini', 'gpt-4o'],
    )

    text_generation_enabled = st.sidebar.checkbox(
        'Generate text using '+ model_name,
        value=True
    )

    image_generation_enabled = st.sidebar.checkbox(
        'Generate image using OpenAI DALL-E',
        value=False
    )

if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]

for msg in st.session_state.messages:
    if "role" in msg and "content" in msg:
        # display text
        st.chat_message(msg["role"]).write(msg["content"])
    if "type" in msg and msg["type"]=="image":
        # display image
        st.image(msg["data"])

if prompt := st.chat_input():
    if not openai_api_key:
        st.info("To continue, please put your OpenAI API key in an environment variable.")
        st.stop()

    client = OpenAI(api_key=openai_api_key)

    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    if text_generation_enabled:
        # get the prompt message to send to OpenAI API
        prompt_message = [st.session_state.messages[-1]]
        print("Sending prompt to OpenAI API:")
        print(prompt_message)

        response = client.chat.completions.create(model=model_name, messages=prompt_message)

        # alternative: send all messages to the OpenAI API
        #response = client.chat.completions.create(model=model_name, messages=st.session_state.messages)
        print(response)

        response_message = response.choices[0].message.content

        st.session_state.messages.append({"role": "assistant", "content": response_message})
        st.chat_message("assistant").write(response_message)

    if image_generation_enabled:
        generating_image_msg = "Generating image based on \"" + prompt + "\"..."
        st.session_state.messages.append({"role": "assistant", "content": generating_image_msg})
        st.chat_message("assistant").write(generating_image_msg)

        # use OpenAI image generation model
        response = client.images.generate(model="dall-e-2", prompt=prompt, size="512x512")
        st.session_state.messages.append({"type": "image", "data": response.data[0].url})
        st.image(response.data[0].url)
