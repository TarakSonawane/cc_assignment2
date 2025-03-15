from azure.storage.blob import BlobServiceClient
import os

# Load Azure Storage Credentials
STORAGE_ACCOUNT_NAME = os.getenv("AZURE_BLOB_ACCOUNT", "productcatalougeblob")
STORAGE_ACCOUNT_KEY = os.getenv("AZURE_BLOB_KEY")
CONTAINER_NAME = os.getenv("AZURE_BLOB_CONTAINER", "product-images")

# Create Blob Service Client
blob_service_client = BlobServiceClient(
    f"https://{STORAGE_ACCOUNT_NAME}.blob.core.windows.net",
    credential=STORAGE_ACCOUNT_KEY
)

def upload_image(image_file, image_name):
    """Uploads an image to Azure Blob Storage and returns the URL."""
    blob_client = blob_service_client.get_blob_client(container=CONTAINER_NAME, blob=image_name)
    blob_client.upload_blob(image_file, overwrite=True)

    # Return URL
    return f"https://{STORAGE_ACCOUNT_NAME}.blob.core.windows.net/{CONTAINER_NAME}/{image_name}"
