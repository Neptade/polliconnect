import os
import time
import psutil
from datetime import datetime
from azure.storage.blob import BlobServiceClient
from dotenv import load_dotenv
from picamera import PiCamera

load_dotenv()

PHOTO_DIR = "/home/pi/photos"
AZURE_CONNECTION_STRING = os.getenv('AZURE_STORAGE_CONNECTION_STRING')
CONTAINER_NAME = "clientpictures"
CAPTURE_DURATION = 300
CAPTURE_INTERVAL = 5  # Augmenté à 5 secondes

os.makedirs(PHOTO_DIR, exist_ok=True)

blob_service_client = BlobServiceClient.from_connection_string(AZURE_CONNECTION_STRING)
container_client = blob_service_client.get_container_client(CONTAINER_NAME)

camera = PiCamera()

def check_resources():
    cpu_percent = psutil.cpu_percent()
    memory_percent = psutil.virtual_memory().percent
    disk_percent = psutil.disk_usage('/').percent
    if cpu_percent > 90 or memory_percent > 90 or disk_percent > 90:
        print(f"Resource usage high: CPU {cpu_percent}%, Memory {memory_percent}%, Disk {disk_percent}%")
        return False
    return True

def take_photos(duration, interval):
    print(f"Taking photos for {duration} seconds...")
    start_time = time.time()
    photo_paths = []
    
    while time.time() - start_time < duration:
        if not check_resources():
            print("Resource usage too high, pausing capture")
            time.sleep(10)
            continue
        
        timestamp = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
        filename = f"photo_{timestamp}.jpg"
        filepath = os.path.join(PHOTO_DIR, filename)
        try:
            camera.capture(filepath)
            print(f"Photo taken: {filepath}")
            photo_paths.append(filepath)
        except Exception as e:
            print(f"Error capturing photo: {e}")
        time.sleep(interval)
    
    return photo_paths

def upload_and_delete_photo(filepath):
    try:
        print(f"Uploading photo: {filepath}")
        blob_name = os.path.basename(filepath)
        blob_client = container_client.get_blob_client(blob_name)
        
        with open(filepath, "rb") as data:
            blob_client.upload_blob(data)
        print(f"Photo uploaded: {blob_name}")
        
        os.remove(filepath)
        print(f"Photo deleted: {filepath}")
    except Exception as e:
        print(f"Error processing {filepath}: {e}")

def main():
    while True:
        try:
            photo_paths = take_photos(CAPTURE_DURATION, CAPTURE_INTERVAL)
            
            print(f"Uploading {len(photo_paths)} photos...")
            for photo_path in photo_paths:
                if os.path.exists(photo_path) and os.path.getsize(photo_path) > 0:
                    upload_and_delete_photo(photo_path)
                else:
                    print(f"Error: Photo {photo_path} does not exist or is empty")
            
            print("All photos processed. Starting next capture cycle...")
            time.sleep(5)  # Pause before starting next cycle

        except Exception as e:
            print(f"Une erreur est survenue : {e}")
            time.sleep(10)  # Longer wait time in case of error

if __name__ == "__main__":
    try:
        main()
    finally:
        camera.close()