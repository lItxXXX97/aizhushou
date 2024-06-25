from langchain.chains import ConversationChain
from langchain_openai import ChatOpenAI
import os
# from langchain.memory import ConversationBufferMemory

os.environ["OPENAI_BASE_URL"] = "https://api.aigc369.com/v1"
def get_chat_response(prompt, memory, openai_api_key):
    model = ChatOpenAI(model="gpt-3.5-turbo", openai_api_key=openai_api_key)
    chain = ConversationChain(llm=model, memory=memory)

    response = chain.invoke({"input":prompt})
    return response["response"]
# memory= ConversationBufferMemory(return_messages=True)
# print(get_chat_response("牛顿提出过哪些知名的定律？", memory,os.getenv("OPENAI_API_KEY")))
# print(get_chat_response("我上一个问题是什么？", memory,os.getenv("OPENAI_API_KEY")))