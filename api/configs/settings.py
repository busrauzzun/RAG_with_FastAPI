from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_DATABASE: str = 'api'
    DATABASE_DRIVER: str = 'ODBC Driver 17 for SQL Server'
    DATABASE_SERVER: str = 'LAPTOP-1HG5QA9G'
    OPENAI_API_KEY:str
    DATABASE_URL:str


    class Config:
        env_file = r'/.env'
        env_file_encoding = 'utf-8'



