from jinja2 import FileSystemLoader, Environment
from langchain_core.chat_history import BaseChatMessageHistory, InMemoryChatMessageHistory
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnableWithMessageHistory
from api.services.vectrodb_llm_service import create_vectordb, create_llm
import os
from sqlalchemy.orm import Session
from api.services.log_service import get_logs

def get_session_history(session_id:str, db:Session)-> BaseChatMessageHistory:
    chat_history = InMemoryChatMessageHistory()
    logs = get_logs(db, session_id)

    for log in logs:
        chat_history.add_message(HumanMessage(content=log.user_question))
        chat_history.add_message(AIMessage(content=log.chatbot_response))

    return chat_history
def get_answer(question, session_id, db:Session):
    try:
        vectordb = create_vectordb()
        llm = create_llm()

        retriever = vectordb.as_retriever(search_type='similarity')
        retrieved_docs = retriever.invoke(question)

        context_list = [doc.page_content for doc in retrieved_docs]
        context = " ".join(context_list)

        data = {'context': context}
        env = Environment(loader=FileSystemLoader(os.path.join(os.path.dirname(__file__), '..', 'models', 'schemas')))
        template = env.get_template("prompt_template.jinja2")
        prompt_template = template.render(data)

        prompt = ChatPromptTemplate.from_messages(
            [
                ("system", prompt_template),
                MessagesPlaceholder(variable_name='messages')
            ]
        )

        chain = prompt | llm
        config = {'configurable': {'session_id': session_id}}
        with_message_history = RunnableWithMessageHistory(chain,lambda _: get_session_history(session_id,db))
        response = with_message_history.invoke([HumanMessage(content=question)], config=config)
        answer = response.content
        response = {
            "answer": answer,
            "retrieved_documents": retrieved_docs
        }
        return response

    except Exception as e:
        return {"error": f"LLM'den sonuç gelmedi. {str(e)}"}