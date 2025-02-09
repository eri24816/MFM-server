import traceback
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import base64
from pydantic import BaseModel
import json
import serial

COM_PORT = 'COM3'
BAUD_RATE = 9600

ser = serial.Serial(COM_PORT, BAUD_RATE)

class ImageData(BaseModel):
    image: str  # base64 encoded image

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

@app.post("/analyze-notation")
async def analyze_notation(request: Request):
    """Process base64 encoded image data"""
    
    from .notation_to_parameter import notation_to_parameters
    import numpy as np
    try:
        # Print raw request body
        body = await request.body()
        body = json.loads(body.decode('utf-8'))
        image_bytes = base64.b64decode(body['image'])
        parameters :dict = notation_to_parameters(image_bytes)
        parameters['control_length'] = parameters['intensity'].shape[1]
        for key, value in parameters.items():
            if type(value) is np.ndarray:
                # use base64 for array values
                parameters[key] = value.astype(np.float32).tobytes()
                parameters[key] = base64.b64encode(parameters[key]).decode('utf-8')
            
        return parameters
    
    except Exception as e:
        traceback.print_exc()
        raise e
    
@app.get("/serial")
async def serial_read():
    line = ''
    while ser.in_waiting > 0:
        line = ser.readline().decode('utf-8').strip()
    line = line.replace('\t', ' ')
    print(line)
    return line

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)