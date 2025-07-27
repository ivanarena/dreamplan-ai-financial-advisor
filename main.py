from fastapi import FastAPI, Request, Cookie, Body
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from uuid import uuid4
from contextlib import asynccontextmanager
from time import time
from components.chat import chat
from db import connect_db, disconnect_db, insert_reply, insert_feedback


@asynccontextmanager
async def lifespan(app: FastAPI):
    await connect_db()
    try:
        yield
    finally:
        try:
            await disconnect_db()
        except Exception as e:
            print(f"Error during disconnect_db: {e}")


app = FastAPI(lifespan=lifespan)
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")
sessions = {}


@app.get("/", response_class=HTMLResponse)
async def index(request: Request, session_id: str = Cookie(default=None)):
    if not session_id:
        session_id = str(uuid4())
        response = templates.TemplateResponse("index.html", {"request": request})
        response.set_cookie("session_id", session_id)
        return response
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/chat")
async def chat_endpoint(request: Request, session_id: str = Cookie(default=None)):
    data = await request.json()
    message = data.get("message", "")

    if not session_id:
        return JSONResponse({"error": "Session ID not set."}, status_code=400)

    history = sessions.get(session_id, [])
    history.append({"role": "user", "content": message})

    start_time = time()
    reply = await chat(history)
    end_time = time()
    history.append({"role": "assistant", "content": reply})

    # Keep last 10 user+assistant pairs (20 messages)
    if len(history) > 20:
        history = history[-20:]
    sessions[session_id] = history

    await insert_reply(
        session_id=session_id,
        query=message,
        response=reply,
        response_time=int((end_time - start_time) * 1000),
    )

    return JSONResponse({"reply": reply, "session_id": session_id})


@app.post("/feedback")
async def feedback_endpoint(request: Request, payload: dict = Body(...)):
    session_id = payload.get("session_id") or request.cookies.get("session_id")
    if not session_id:
        return JSONResponse({"error": "Session ID not set."}, status_code=400)

    feedback = {
        "correctness": payload.get("correctness"),
        "relevance": payload.get("relevance"),
        "clarity": payload.get("clarity"),
        "satisfaction": payload.get("satisfaction"),
        "comments": payload.get("comments", ""),
    }

    await insert_feedback(session_id=session_id, feedback=feedback)
    sessions.pop(session_id, None)

    # Generate a new session ID
    new_session_id = str(uuid4())

    # Return response with new session_id cookie
    response = JSONResponse({"status": "success", "new_session_id": new_session_id})
    response.set_cookie("session_id", new_session_id)
    return response
