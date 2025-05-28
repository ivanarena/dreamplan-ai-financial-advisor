from fastapi import FastAPI, Request, Cookie
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from uuid import uuid4

from pipeline import pipeline

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

chats = {}


@app.get("/", response_class=HTMLResponse)
async def index(request: Request, session_id: str = Cookie(default=None)):
    if not session_id:
        session_id = str(uuid4())
        response = templates.TemplateResponse("index.html", {"request": request})
        response.set_cookie("session_id", session_id)
        print(f"New session created: {session_id}")
        return response
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/chat")
async def chat_endpoint(request: Request, session_id: str = Cookie(default=None)):
    data = await request.json()
    message = data.get("message", "")
    print(f"Received message: {message}")

    if not session_id:
        return JSONResponse({"error": "Session ID not set."}, status_code=400)

    history = chats.get(session_id, [])
    history.append({"role": "user", "content": message})
    print(f"Current chat history for session {session_id}: {history}")
    reply = await pipeline(history)
    print(f"Generated reply: {reply}")
    history.append({"role": "assistant", "content": reply})
    chats[session_id] = history

    return JSONResponse({"reply": reply})
