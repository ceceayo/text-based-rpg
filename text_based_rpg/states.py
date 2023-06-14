import pynecone as pc
import string, secrets
from typing import Optional
from .game import *
class BaseState(pc.State):
    '''
    Represents the BaseState, this makes it possible in the future to create multiple States.
    Inherit from BaseState
    '''
    ...
class LoggingState(BaseState):
    options: list[str]
    selected_option: str
    logs: list[str]
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.options = ['a', 'b']
        self.logs += ['hi', 'it works!']


    def use_option(self, option):
        if option not in self.options: raise "option not in self.options!"
        self.logs.append(f"used option {option}.")

class UserInformation(BaseState):
    name: str
    _name_legal: bool = False # backend var
    key1: str
    key2: str
    """
    keys part
    a user has two keys, consisting of 64 bits of random nonsense,
    with which the user can be identified in the database.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.generate_new_key_pair()
    def change_name(self, new_name: str):
        self.name = new_name.title()
        self.name_legal= True

    def generate_new_key_pair(self):
        letters = string.ascii_lowercase
        result_str = ''.join(secrets.choice(letters) for _ in range(64))
        self.key1 = result_str
        del result_str
        result_str = ''.join(secrets.choice(letters) for _ in range(64))
        self.key2 = result_str

class GameInformation(BaseState):
    _game: Optional[Game]
    _started: bool