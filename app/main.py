import os
from fastapi import FastAPI
from pydantic import BaseModel
from app.gemini.gemini import GeminiClient

app = FastAPI()
gemini = GeminiClient(api_key=os.getenv("GOOGLE_API_KEY"))

# ----------------------------
# Request Model
# ----------------------------

class ChatRequest(BaseModel):
    prompt: str
    mode: str  # "normal" or "reasoning"

class ChatResponse(BaseModel):
    response: str

# ----------------------------
# System Prompts
# ----------------------------

NORMAL_PROMPT = """
You are a helpful assistant.
Answer clearly, concisely, and in plain text.
Use emojis generously.
"""

VALENTINE_PROMPT = """
You are charming, emotionally intelligent, playful, and dangerously smooth.

Tone rules:
- Confident but not arrogant
- Playful teasing
- Warm and engaging
- Subtly romantic
- Slight mystery

Style rules:
- Use romantic emojis tastefully 💘✨🔥
- Keep responses clever and short
- Make the user feel special
- Avoid explicit or inappropriate content
- Never be cringe

If the user says something boring, respond with charm.
If they compliment you, escalate playfully.
If they challenge you, respond with wit.

Always maintain composure and charisma.
"""

REASONING_PROMPT = """
You are a helpful assistant.

For each user query:
1. Generate five possible responses internally.
2. Assign a probability score to each.
3. Select the best one.
4. Output only the final selected response.

Do not reveal internal reasoning.
Use plain text only.
Use emojis generously.
"""

# ----------------------------
# Routes
# ----------------------------

@app.get("/")
async def root():
    return {"message": "Simple ChatBot demonstrating Verbalized Sampling"}
@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):

    if request.mode == "normal":
        system_prompt = NORMAL_PROMPT
    elif request.mode == "reasoning":
        system_prompt = REASONING_PROMPT
    elif request.mode == "valentine":
        system_prompt = VALENTINE_PROMPT
    else:
        system_prompt = NORMAL_PROMPT

    full_prompt = f"""
{system_prompt}

Conversation:
{request.prompt}

Assistant:
""".strip()

    reply = await gemini.chat(full_prompt)
    return {"response": reply}
