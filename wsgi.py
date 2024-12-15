from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routers import upload_doc, chat, show_collection


def create_app() -> FastAPI:
    app = FastAPI(
        title = 'Uni Rag',
        description='Api for KBU'
    )
    init_routers(app)
    configure_middlewares(app)
    return(app)

def init_routers(app:FastAPI) -> None:
    app.include_router(upload_doc.router)
    app.include_router(show_collection.router)
    app.include_router(chat.router)


def configure_middlewares(app:FastAPI) -> None:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=['*'],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"]
    )

app = create_app()