import streamlit as st
from langchain.memory import ConversationBufferMemory
from pdf_qatool.utils import qa_agent

st.title("📑 AI智能PDF问答工具")
with st.sidebar:
    openai_api_key = st.text_input("请输入你的Openai API Key:", type="password")
    st.markdown("[获取OpenAI API key](https://platform.openai.com/account/api-keys)")
if "memory" not in st.session_state:
    st.session_state["memory"] = ConversationBufferMemory(
        return_messages=True,
        memory_key="chat_history",
        output_key="answer"
    )
uploaded_file = st.file_uploader("上传你的PDF文件：", type="pdf")
question = st.text_input("对PDF的内容进行提问", disabled=not uploaded_file)

if uploaded_file and question and not openai_api_key:
    st.info("请输入你的OpenAI API密钥")

if uploaded_file and question and openai_api_key:
    with st.spinner("AI正在思考中，请稍等..."):
        response = qa_agent(openai_api_key, st.session_state["memory"],
                            uploaded_file, question)
    st.markdown("### 答案")
    st.write(response["answer"])
    st.session_state["chat_history"] = response["chat_history"]

if "chat_history" in st.session_state:
    with st.expander("历史消息"):
        for i in range(0, len(st.session_state["chat_history"]), 2):
            human_messages = st.session_state["chat_history"][i]
            ai_messages = st.session_state["chat_history"][i+1]
            st.write(human_messages.content)
            st.write(ai_messages.content)
            if i < len(st.session_state["chat_history"]) - 2:
                st.divider()