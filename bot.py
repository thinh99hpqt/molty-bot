from fastapi import FastAPI
from pydantic import BaseModel
import random

app = FastAPI()

game_memory = {}

class GameState(BaseModel):
    game_id: str
    turn: int
    hp: int
    enemy_hp: int
    enemies_nearby: int


@app.get("/")
def health_check():
    return {"status": "alive"}


@app.post("/move")
def make_move(state: GameState):

    if state.game_id not in game_memory:
        game_memory[state.game_id] = {
            "total_turns": 0,
            "last_action": None
        }

    memory = game_memory[state.game_id]
    memory["total_turns"] += 1

    if state.turn < 5 and state.enemies_nearby == 0:
        action = "search"

    elif state.hp < 30 and state.enemy_hp < 25:
        action = "attack"

    elif state.hp < 30:
        action = "retreat"

    elif state.enemies_nearby > 1:
        action = "retreat"

    elif state.hp > state.enemy_hp:
        action = "attack"

    else:
        action = random.choice(["attack", "move"])

    memory["last_action"] = action

    return {
        "action": action,
        "memory": memory
    }
