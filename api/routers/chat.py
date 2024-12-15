from fastapi import APIRouter, Request, HTTPException, Depends
from requests import Session
from api.models import models
from api.models.models import get_db
from api.models.schemas.question_request import QuestionRequest
from api.services.chat_service import get_answer
from api.configs.logger.logger import RagLogger
from api.configs.constants import OperationNames, StatusCodes, ErrorMessages
from api.services.log_service import create_log

models.create_tables()
operation_logger = RagLogger('chat_service')
router = APIRouter()
#Bu router'a her gidildiğinde get_db fonksiyonu ile veritabanı oturumu oluşturulur.
@router.post("/chat")
async def chat(request: QuestionRequest, fastapi_request: Request, db: Session = Depends(get_db)):
    operation_log = operation_logger.start_service_operation(operation_name=OperationNames.CHAT, request=fastapi_request)
    try:
        question = request.question
        operation_log.add_field('input_question',question)

        session_id = request.session_id
        operation_log.add_field('session_id', session_id)

        result = get_answer(question, session_id,db)
        operation_log.add_field('result', result["answer"])
        operation_log.succeed()
        create_log(db=db,user_question=question, chatbot_response=result['answer'], session_id=session_id)
        return {
            "answer": result["answer"],
            'retrieved_contents': result["retrieved_documents"],
            "session_id":session_id,
            'status_code':StatusCodes.SUCCESS
        }
    except Exception as e:
        operation_log.fail(exc_info=e)
        raise HTTPException(
            status_code=StatusCodes.INTERNAL_SERVER_ERROR,
            detail= {
                'message': ErrorMessages.PROCESSING_ERROR
            }
        )

