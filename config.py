import os

class Config:
    # Azure SQL Database Connection
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")

    # Azure Blob Storage Configuration
    BLOB_STORAGE_ACCOUNT = os.getenv("AZURE_BLOB_ACCOUNT")
    BLOB_STORAGE_KEY = os.getenv("AZURE_BLOB_KEY")
    BLOB_CONTAINER_NAME = os.getenv("AZURE_BLOB_CONTAINER")
