from langchain.chains import ConversationalRetrievalChain
from langchain_openai import ChatOpenAI
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai.embeddings import OpenAIEmbeddings

import os

os.environ["OPENAI_BASE_URL"] = "https://api.aigc369.com/v1"

def qa_agent(openai_api_key, memory, uploaded_file, question):
    model = ChatOpenAI(model="gpt-3.5-turbo", openai_api_key=openai_api_key, temperature=0.0)
    file_content = uploaded_file.read()
    temp_file_path = "temp.pdf"
    with open(temp_file_path, "wb") as temp_file:
        temp_file.write(file_content)
    loader = PyPDFLoader(temp_file_path)
    docs = loader.load()
    text_splitters = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=50,
        separators=["\n\n", "\n", "。", "!", "?", "，", "、", ""]
    )
    texts = text_splitters.split_documents(docs)
    embeddings_model = OpenAIEmbeddings()
    db = FAISS.from_documents(texts, embeddings_model)
    retriever = db.as_retriever()
    qa = ConversationalRetrievalChain.from_llm(
        llm=model,
        retriever=retriever(search_kwargs={"k":1}),
        memory=memory
    )
    response = qa.invoke({"chat_history": memory,
                         "question": question})
    return response