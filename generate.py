import requests
import base64
import os

api_endpoint = 'http://localhost:11434/api/generate'

llama_data = {
    'model': 'llama2',
    'stream': False,
    'prompt': 'Act as a translator machine. Translate this to spanish: car.'
}

def handle_llama2_generate():
    llama_data['prompt'] = input("Enter your prompt for llama2:")
    call_api_generate(api_endpoint, llama_data)
    return

def handle_llava_image_recognition():
    examine_photos()
    return

def call_api_generate(api_endpoint, data):
    response = requests.post(api_endpoint, json=data)

    if response.status_code == 200:
        response_data =  response.json()
        # print(response_data)
        print(f"{response_data['response']}\n")
        return
    print('Failed to get a response from Ollama API')
    return

def examine_photos():
    files = None
    try:
        images_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'images')
        files = os.listdir(images_dir)
    except Exception as e:
        print(f"Problem listing the files in dir: {images_dir}\n{e}")
    if files is not None:
        jpg_files = [f for f in files if f.lower().endswith('.jpg')]
        for f in jpg_files:
            print(os.path.join(images_dir, f))
            with open(os.path.join(images_dir, f), 'rb') as image_file:
                #1. read its contents (binary)
                image_data = image_file.read()

                #2. turn binary into base64
                base64_image_data = base64.b64encode(image_data)

                #3. encode to utf-8
                base64_image_string = base64_image_data.decode('utf-8') 
                llava_data = {
                    'model': 'llava',
                    'stream': False,
                    'prompt': 'Describe the image provided',
                    'images': [base64_image_string]
                }
                call_api_generate(api_endpoint, llava_data)
                print('##################################################')
            return

def main_menu():
    while True:
        menu = "How can I assist you?\n" \
        "\t1. Llama2 generate response.\n" \
        "\t2. Llava image generate reconginition.\n" \
        "\t9. Bye.\n"
        num = int(input(menu))
        if num == 1:
            handle_llama2_generate()
        elif num == 2:
            handle_llava_image_recognition()
        elif num == 9:
            break
        else: 
            print("Invalid respone. Try again...\n")
        continue_prompt = "Would you like to continue (Y/N)?"
        if input(continue_prompt).upper() == "N":
            break

main_menu()