import os
import logging
import json
import numpy as np
import torch
from torch import nn

def init():
    """
    This function is called when the container is initialized/started, typically after create/update of the deployment.
    You can write the logic here to perform init operations like caching the model in memory
    """
    global model
    global device

    # Set the device
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

    # AZUREML_MODEL_DIR is an environment variable created during deployment.
    # It is the path to the model folder (./azureml-models/$MODEL_NAME/$VERSION)
    model_path = os.path.join(
        os.getenv("AZUREML_MODEL_DIR"), "hotShotNN/1/modelHotShot5epochs.pth"
    )

    # Load the model
    model = torch.load(model_path, map_location=device)
    model.eval()
    logging.info("Init complete")


def run(raw_data):
    """
    This function is called for every invocation of the endpoint to perform the actual scoring/prediction.
    In the example, we extract the data from the JSON input and call the PyTorch model's forward method
    and return the result back
    """
    try:
        logging.info("Request received")

        # Parse the input data
        data = json.loads(raw_data)["data"]
        data = np.array(data).astype(np.float32)

        # Convert to torch tensor
        inputs = torch.from_numpy(data).to(device)

        # Ensure the model is in evaluation mode and disable gradient calculation
        with torch.no_grad():
            outputs = model(inputs)

        # Convert the output tensor to a list
        result = outputs.cpu().numpy().tolist()
        
        logging.info("Request processed successfully")
        return json.dumps({"result": result})
    except Exception as e:
        error = str(e)
        logging.error(f"Error: {error}")
        return json.dumps({"error": error})
