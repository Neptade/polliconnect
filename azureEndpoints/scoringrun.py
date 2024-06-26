import os
import json
import torch
import logging

def init():
    global model
    # Define the path to the model
    model_path = os.path.join(os.getenv('AZUREML_MODEL_DIR'), 'best.pt')
    # Load the model
    model = torch.load(model_path)
    logging.info("Init complete")

def run(data):
    logging.info("model 1: request received")
    try:
        # Parse the input data
        input_data = json.loads(data)
        # Convert input data to a PyTorch tensor
        input_tensor = torch.tensor(input_data, dtype=torch.float32)
        # Make predictions
        with torch.no_grad():
            output = model(input_tensor)
        # Convert output to list and return as JSON
        result = output.tolist()
        logging.info("model 1: request processed")
        return json.dumps(result)
    except Exception as e:
         logging.info(e)