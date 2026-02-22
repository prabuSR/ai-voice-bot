from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import requests

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # allow all (for development)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
API_KEY = "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"

class Message(BaseModel):
    message: str

@app.post("/chat")
async def chat(data: Message):
    try:
        url = "https://openrouter.ai/api/v1/chat/completions"

        headers = {
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": "openrouter/auto",
            "messages": [
                {"role": "system", "content": "You are a friendly motivational assistant."},
                {"role": "user", "content": data.message}
            ]
        }

        response = requests.post(url, headers=headers, json=payload)

        result = response.json()

        return {
            "reply": result["choices"][0]["message"]["content"]
        }

    except Exception as e:
        return {"reply": "Error: " + str(e)}
