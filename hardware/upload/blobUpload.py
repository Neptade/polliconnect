import os, uuid
from dotenv import load_dotenv
from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient

load_dotenv()


'''connection block'''

try:
    # account_url = "https://polliconnectstorage.blob.core.windows.net"
    # default_credential = DefaultAzureCredential()

    # # Create the BlobServiceClient object
    # blob_service_client = BlobServiceClient(account_url, credential=default_credential)

    # environment variable into account.
    connect_str = os.getenv('AZURE_STORAGE_CONNECTION_STRING')

    # Create the BlobServiceClient object
    blob_service_client = BlobServiceClient.from_connection_string(connect_str)

    print("logged in")

except Exception as ex:
    
    print('Exception:')
    print(ex)



'''container creation block'''

try:
    #Create a unique name for the container
    container_name = "clientpictures"
    # Create the container
    container_client = blob_service_client.create_container(container_name)

    print("created container")

except Exception as ex:
    print('Exception:')
    print(ex)



'''upload block'''

try:
    # Create a local directory to hold blob data
    local_path = "./hardware/upload/testData"
    #os.mkdir(local_path)

    # Create a file in the local data directory to upload and download
    local_file_name = "test.txt"
    upload_file_path = os.path.join(local_path, local_file_name)

    # Create a blob client using the local file name as the name for the blob
    blob_client = blob_service_client.get_blob_client(container=container_name, blob=local_file_name)

    print("\nUploading to Azure Storage as blob:\n\t" + local_file_name)

    # Upload the file
    with open(file=upload_file_path, mode="rb") as data:
        blob_client.upload_blob(data)

    print("uploaded")

except Exception as ex:
    print('Exception:')
    print(ex)