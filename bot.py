from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class GameState(BaseModel):
    game_id: str
    turn: int
    hp: int
    enemy_hp: int
    enemies_nearby: int

@app.post("/move")
def make_move(state: GameState):

    # Early game: farm
    if state.turn < 5 and state.enemies_nearby == 0:
        return {"action": "search"}

    # Low HP → retreat
    if state.hp < 30:
        return {"action": "retreat"}

    # Too many enemies
    if state.enemies_nearby > 1:
        return {"action": "retreat"}

    # Stronger → attack
    if state.enemies_nearby == 1 and state.hp > state.enemy_hp:
        return {"action": "attack"}

    # Finish weak enemy
    if state.enemy_hp < 20:
        return {"action": "attack"}

    return {"action": "move"}
