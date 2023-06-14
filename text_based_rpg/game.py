from pydantic import BaseModel
from typing import List, Dict

import json
from pydantic.tools import parse_obj_as

class Option(BaseModel):
    text: str
    to_room: str

class Room(BaseModel):
    texts: List[str]
    options: List[Option]

class Game(BaseModel):
    rooms: Dict[str, Room]

def load_game(game_file: str):
    loaded_json = json.loads(game_file)
    game = parse_obj_as(Game, loaded_json)
    return game