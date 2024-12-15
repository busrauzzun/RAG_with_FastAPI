import tempfile
import uuid
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from api.configs.constants import SplitParameters
from api.services.vectrodb_llm_service import create_vectordb

chunk_size = SplitParameters.CHUNK_SIZE
chunk_overlap = SplitParameters.CHUNK_OVERLAP
current_docs = []

def load_document(file):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:  # Dosya yoluna ulaşmak için.
        temp_file.write(file.read())
        temp_file_path = temp_file.name
    loader = PyPDFLoader(temp_file_path)
    doc = loader.load()
    return doc

def upload_docs_to_vectordb(doc):
    try:
        vectordb = create_vectordb()
        current_docs.clear()
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            separators=["\n\n", "\n", ".", " ", ""]
        )
        chunks = text_splitter.split_documents(doc)
        chunk_ids = [str(uuid.uuid4()) for _ in chunks]

        current_docs.extend(chunks)
        vectordb.add_documents(current_docs, ids=chunk_ids)
        counts = {'chunk_counts': len(chunks), 'vectordb_chunk_counts': vectordb._collection.count()}
        return counts

    except Exception as e:
        print("Dokumanlar vectordb'ye yuklenemedi.")
