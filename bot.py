from fastapi import FastAPI
from pydantic import BaseModel
import random

app = FastAPI()

# Memory lưu trạng thái theo game_id
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

    # Lưu lịch sử theo game
    if state.game_id not in game_memory:
        game_memory[state.game_id] = {
            "total_turns": 0,
            "last_action": None
        }

    memory = game_memory[state.game_id]
    memory["total_turns"] += 1

    # ===== AI LOGIC =====

    # Early farm strategy
    if state.turn < 5 and state.enemies_nearby == 0:
        action = "search"

    # Low HP but enemy yếu -> all-in
    elif state.hp < 30 and state.enemy_hp < 25:
        action = "attack"

    # Low HP retreat
    elif state.hp < 30:
        action = "retreat"

    # Nhiều enemy -> retreat
    elif state.enemies_nearby > 1:
        action = "retreat"

    # Stronger than enemy -> attack
    elif state.hp > state.enemy_hp:
        action = "attack"

    # Random tactical decision
    else:
        action = random.choice(["attack", "move"])

    memory["last_action"] = action

    return {
        "action": action,
        "memory": memory
    }
