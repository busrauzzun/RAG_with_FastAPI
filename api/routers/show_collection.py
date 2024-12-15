from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import RedirectResponse
from api.configs.logger.logger import RagLogger
from api.configs.constants import OperationNames, StatusCodes, ErrorMessages

router = APIRouter()
operation_logger = RagLogger('show_coll_Service')

@router.get("/collection")
async def show_collection(request: Request):
    operation_log = operation_logger.start_service_operation(operation_name=OperationNames.SHOW_COLLECTION, request=request)
    try:
        response = RedirectResponse(url="http://localhost:3000/collections/documents")
        operation_log.succeed()
        return response

    except Exception as e:
        operation_log.fail(exc_info=e)
        raise HTTPException(status_code=StatusCodes.INTERNAL_SERVER_ERROR,
                            detail= {
                                'message': ErrorMessages.GENERIC_ERROR
                            })





"""
Chromadb ui kullanmak istemeyince:
try:

        result = vectordb.get(include=["documents", "metadatas"])
        documents = result.get("documents", [])
        metadatas = result.get("metadatas", [])
        ids = result.get("ids", [])
        collection_info = []
        for doc, metadata, doc_id in zip(documents, metadatas, ids):
            collection_info.append({
                "id": doc_id,
                "page_content": doc,
                "metadata": metadata
            })

        return {"collection": collection_info}

    except Exception as e:
        return {"error": f"Collection gosterilemedi: {str(e)}"}
"""

#docker run -p 8001:8000 ghcr.io/chroma-core/chroma:latest
#docker run -p 3000:3000 fengzhichao/chromadb-admin