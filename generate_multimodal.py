import requests
import base64

# load image
with open(r'C:\Users\bamal\Documents\Programming\ollama\images\IMG_0282.JPG', 'rb') as image_file:

    #1. read its contents (binary)
    image_data = image_file.read()

    #2. turn binary into base64
    base64_image_data = base64.b64encode(image_data)

    #3. encode to utf-8
    base64_image_string = base64_image_data.decode('utf-8')
    

api_endpoint = 'http://localhost:11434/api/generate'

data = {
    'model': 'llava',
    'stream': False,
    'prompt': 'Describe the image provided',
    'images': [base64_image_string]
}

response = requests.post(api_endpoint, json=data)

if response.status_code == 200:
    response_data = response.json()
    print(response_data['response'])

else:
    print('Failed to get response from Ollama API')