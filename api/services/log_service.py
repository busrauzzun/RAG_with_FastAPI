from api.models.models import Log
from sqlalchemy.orm import Session

def create_log(db: Session, user_question:str, chatbot_response:str, session_id:str): #Log tablosuna yeni kayıt ekler.
    new_log = Log(
        user_question=user_question,
        chatbot_response= chatbot_response,
        session_id = session_id
    )

    db.add(new_log)
    db.commit() #Db'ye değişiklikleri kaydeder.


def get_logs(db: Session, session_id: str): #O session_id yi içeren kayıtları döndürür.

    return db.query(Log).filter(Log.session_id == session_id).order_by(Log.datetime.asc()).all()
