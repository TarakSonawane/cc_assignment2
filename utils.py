from azure.storage.blob import BlobServiceClient
from config import Config
import uuid

blob_service_client = BlobServiceClient(
    account_url=f"https://{Config.BLOB_STORAGE_ACCOUNT}.blob.core.windows.net",
    credential=Config.BLOB_STORAGE_KEY
)

def upload_to_blob(image):
    blob_name = f"{uuid.uuid4()}_{image.filename}"  # Unique name
    blob_client = blob_service_client.get_blob_client(container=Config.BLOB_CONTAINER_NAME, blob=blob_name)
    blob_client.upload_blob(image, overwrite=True)
    return f"https://{Config.BLOB_STORAGE_ACCOUNT}.blob.core.windows.net/{Config.BLOB_CONTAINER_NAME}/{blob_name}"
