import os, uuid
from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient

try:
    print("Azure Blob Storage Python quickstart sample")

    account_url = "https://polliconnectstorage.blob.core.windows.net"
    default_credential = DefaultAzureCredential()

    # Create the BlobServiceClient object
    blob_service_client = BlobServiceClient(account_url, credential=default_credential)

    print("logged in")

    # Create a unique name for the container
    container_name = "clientpictures"
    # Create the container
    container_client = blob_service_client.create_container(container_name)

    print("created container")

    # Create a local directory to hold blob data
    local_path = "./hardware/upload/testData"
    os.mkdir(local_path)

    # Create a file in the local data directory to upload and download
    local_file_name = "test.txt"
    upload_file_path = os.path.join(local_path, local_file_name)

    # Write text to the file
    file = open(file=upload_file_path, mode='w')
    file.write("testtext")
    file.close()

    print("created file")

    # Create a blob client using the local file name as the name for the blob
    blob_client = blob_service_client.get_blob_client(container=container_name, blob=local_file_name)

    print("\nUploading to Azure Storage as blob:\n\t" + local_file_name)

    # Upload the created file
    with open(file=upload_file_path, mode="rb") as data:
        blob_client.upload_blob(data)

    print("uploaded")

except Exception as ex:
    
    print('Exception:')
    print(ex)