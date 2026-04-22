from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

# Allow all origins for development. In production, restrict this.
origins = [
    "http://127.0.0.1:5500", # Example for Live Server in VS Code
    "http://localhost:5500",
    "http://127.0.0.1:8000", # If the frontend is served by FastAPI itself
    "http://localhost:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allows all headers
)

# In-memory store for game state
game_state = {
    "high_score": 0,
    "last_score": 0,
    "games_played": 0,
}

class ScoreUpdate(BaseModel):
    score: int

@app.get("/")
async def root():
    return {"message": "Welcome to the Snake Game Backend!"}

@app.get("/status")
async def get_status():
    return {"status": "ok", "message": "Backend is running"}

@app.get("/high_score")
async def get_high_score():
    """Retrieves the current high score."""
    return {"high_score": game_state["high_score"]}

@app.post("/game/end")
async def game_end(score_update: ScoreUpdate):
    """Submits the final score of a game."""
    score = score_update.score
    game_state["last_score"] = score
    game_state["games_played"] += 1

    if score > game_state["high_score"]:
        game_state["high_score"] = score
        return {"message": "New high score!", "score": score, "high_score": game_state["high_score"]}
    else:
        return {"message": "Game over, score recorded.", "score": score, "high_score": game_state["high_score"]}

# To run this: uvicorn main:app --reload