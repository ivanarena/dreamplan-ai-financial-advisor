from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pipeline import pipeline
from uuid import uuid4
from fastapi import Cookie

# Very simple memory store
app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

chats = {}


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/chat")
async def chat_endpoint(request: Request, session_id: str = Cookie(default=None)):
    data = await request.json()
    message = data.get("message", "")

    if not session_id:
        session_id = str(uuid4())
        response = JSONResponse({"reply": ""})
        response.set_cookie("session_id", session_id)
        return response

    history = chats.get(session_id, [])
    history.append({"role": "user", "content": message})
    reply = await pipeline(history)
    history.append({"role": "assistant", "content": reply})
    chats[session_id] = history

    return JSONResponse({"reply": reply})
