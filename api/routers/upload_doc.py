from fastapi import APIRouter, UploadFile, File, Request, HTTPException
from api.configs.logger.logger import RagLogger
from api.services.upload_service import load_document, upload_docs_to_vectordb
from api.configs.constants import OperationNames, ErrorMessages

router = APIRouter()
operation_logger = RagLogger('upload_service')

@router.get("/")
async def read_root():
    return {"message": "API çalışıyor"}

@router.post('/upload')
async def upload_doc(file: UploadFile = File(...), request: Request = None):
    operation_log = operation_logger.start_service_operation(operation_name=OperationNames.UPLOAD_DOC, request=request)
    try :

        doc = load_document(file.file)
        counts = upload_docs_to_vectordb(doc)
        operation_log.add_field('yuklenen_chunk_sayisi', counts['chunk_counts'])
        operation_log.succeed()
        return {'message': 'Dokuman veri tabanina kaydedildi',
                'Yuklenen_chunk_sayisi': counts['chunk_counts'],
                "Collection'daki_chunk_sayisi": counts['vectordb_chunk_counts']}
    except Exception as e:
        operation_log.fail(exc_info=e)
        raise HTTPException(status_code=500, detail={
            'message': ErrorMessages.DOCUMENT_UPLOAD_ERROR
        })






