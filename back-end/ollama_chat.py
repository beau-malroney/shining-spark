from langchain_community.llms import Ollama
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory
from langchain.prompts import PromptTemplate
from fastapi import FastAPI, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

app = FastAPI()

# CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# LLM setup
llm = Ollama(model="gemma3")
memory = ConversationBufferMemory()
conversation = ConversationChain(llm=llm, memory=memory)

@app.post("/chat")
async def chat(prompt: str = Form(...)):
    response = conversation.run(prompt)
    return {"response": response}

@app.post("/upload")
async def upload(file: UploadFile):
    content = await file.read()
    filename = file.filename
    # You could parse image/text here and feed to LLM
    return {"status": "received", "filename": filename}
    
if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)
