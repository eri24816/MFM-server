import requests
import base64
from pathlib import Path
import json

def test_notation_analysis(image_path: str, api_url: str = "http://localhost:8000"):
    """
    Test the notation analysis API by sending an image and printing the response.
    
    Args:
        image_path: Path to the image file to analyze
        api_url: Base URL of the API server
    """
    # Read and encode the image
    with open(image_path, 'rb') as image_file:
        image_data = base64.b64encode(image_file.read()).decode('utf-8')
    
    # Prepare the request
    endpoint = f"{api_url}/analyze-notation"
    payload = {
        "image": image_data
    }
    
    try:
        # Send the request
        print(f"Sending request to {endpoint}")
        response = requests.post(endpoint, data=json.dumps(payload).encode('utf-8'))
        response.raise_for_status()
        
        # Process the response
        result = response.json()
        
        # Print some sample data
        print("\nResponse received:")
        print(f"Number of parameters: {len(result)}")
        print("\nKeys in response:", list(result.keys()))
        
        return result
        
    except requests.exceptions.RequestException as e:
        print(f"Error making request: {e}")
        if hasattr(e.response, 'text'):
            print(f"Response text: {e.response.text}")
        return None

if __name__ == "__main__":
    # Example usage
    image_path = Path("W:\\mfm\\MFM_Synthsizer\\data\\notation\\06_A4.png")
    if not image_path.exists():
        print(f"Error: Image file not found at {image_path}")
    else:
        test_notation_analysis(str(image_path)) 