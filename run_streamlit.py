from main import ChatBot
import streamlit as st

bot = ChatBot()
    
st.set_page_config(page_title="Heart Start Intrepid Chat Bot")
with st.sidebar:
    st.title('Heart Start Intrepid Chat Bot')

# Function for generating LLM response
def generate_response(input):
    result = bot.retrievalQA.invoke(input)
    return result

# Store LLM generated responses
if "messages" not in st.session_state.keys():
    st.session_state.messages = [{"role": "assistant", "content": "Welcome, how may I help you!!"}]

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# User-provided prompt
if input := st.chat_input():
    st.session_state.messages.append({"role": "user", "content": input})
    with st.chat_message("user"):
        st.write(input)

# Generate a new response if last message is not from assistant
if st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        with st.spinner("Getting your answer"):
            response = generate_response(input)
            keyword = "Helpful Answer:"
            before_keyword, keyword, after_keyword = response['result'].partition(keyword)
            print(response) 
            st.write(after_keyword) 
    message = {"role": "assistant", "content": after_keyword}
    st.session_state.messages.append(message)