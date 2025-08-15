import os

def text_to_speech(text):
    os.system(f"espeak '{text}'")

text_to_speech("Hello, welcome to the world of text-to-speech synthesis!")

print("Text successfully converted to speech using eSpeak.")