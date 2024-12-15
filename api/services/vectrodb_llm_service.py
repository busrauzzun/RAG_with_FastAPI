from chromadb import HttpClient
from dotenv import load_dotenv
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from api.configs.constants import Models


def create_vectordb():
    load_dotenv()
    directory = './vectordb'
    client = HttpClient(host='localhost', port=8001)
    embedding = OpenAIEmbeddings(model=Models.EMBEDDING_MODEL)
    vectordb = Chroma(client=client, embedding_function=embedding, persist_directory=directory, collection_name='documents')
    return vectordb

def create_llm():
    load_dotenv()
    llm = ChatOpenAI(model=Models.LLM_MODEL)
    return llm
