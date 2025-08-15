# streamlit run .\streamlit_app.py
import streamlit as st
import ollama
from pathlib import Path
import pickle
import pyttsx3

# Text to Speach Class
class ICanSpeak:
    def __init__(self) -> None:
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', 400)
        # self.engine.setProperty('pitch', 0.5)
        self.engine.setProperty('volume', 1.0)
        voices = self.engine.getProperty('voices')
        self.engine.setProperty('voice', voices[1].id)
        pass

    def speakText(self, command):
        # Initialize the engine
        self.engine.say(command) 
        self.engine.runAndWait()
        self.engine.stop()

    def voicesTest(self):
        voices = self.engine.getProperty('voices')
        for v in voices:
            print(v)
        self.engine.say("The voices in my head keep on telling me to pray.") 
        self.engine.runAndWait()
        self.engine.stop()

def read_file_to_variable(filename):
    # Open the file and read its contents
    with open(filename, 'r') as f:
        file_contents = f.read()

    # Return the file contents as a string
    return file_contents

personality = read_file_to_variable('chat_personality.txt')

st.title("Homeboy")
voiceAssistant = ICanSpeak()

if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": personality}]

for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.chat_message(msg["role"], avatar="🧑‍💻").write(msg["content"])
    else:
        st.chat_message(msg["role"], avatar="🤖").write(msg["content"])

with st.sidebar:
    speak_toggle = st.toggle("Speak?")


def generate_response():
    response = ollama.chat(model='llama3', stream=True, messages=st.session_state.messages)
    for partial_resp in response:
        token = partial_resp["message"]["content"]
        st.session_state["full_message"] += token
        yield token

def writeToFile(history):
    Path("./chat_history/").mkdir(parents=True, exist_ok=True)
    f = open("./chat_history/history.txt", "w")
    for h in history:
        f.write(f"{h["role"]} : {h["content"]}\n\n")
    f.close()
    with open("./chat_history/pickled", "wb") as fp:
        pickle.dump(history, fp)

# Function to convert text to speech
def SpeakText(command):
    if speak_toggle:
        voiceAssistant.speakText(command)

if prompt := st.chat_input():
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user", avatar="🧑‍💻").write(prompt)
    st.session_state["full_message"] = ""
    st.chat_message("assistant", avatar="🤖").write_stream(generate_response)
    SpeakText(st.session_state["full_message"])
    st.session_state.messages.append({"role": "assistant", "content": st.session_state["full_message"]})
    writeToFile(st.session_state.messages)