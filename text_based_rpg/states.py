import pynecone as pc
import sqlite3
import string, secrets


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
    name_demo: str
    def set_name_demo(self, newname: str) -> None:
        self.name_demo =newname.title()
        # pc.redirect('/game/')

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

    def change_name(self, data: dict[str, str]):
        if (name := data.get('name')):
            self.name = name.title()
            self.create_session()

    def create_session(self) -> None:
        '''
        Jesse als je dit ziet. Leg aub uit hoe sqlalchemy werkt
        '''
        with sqlite3.connect('pynecone.db') as connection:
            cursor = connection.cursor()
            cursor.execute("SELECT COUNT(*) FROM users WHERE key1=? and key2=?;", (
                self.key1,
                self.key2
            ))
            fetch: int = cursor.fetchone()[0]
            if fetch == 0: # user is new so create a new row
                cursor.execute(
                    '''
                    INSERT INTO users VALUES(?, ?, ?);
                    ''', (self.name, self.key1, self.key2)
                )
                connection.commit()
            else: # user exists
                ...
            cursor.close()
        
                


    def generate_new_key_pair(self):
        letters = string.ascii_lowercase
        result_str = ''.join(secrets.choice(letters) for _ in range(64))
        self.key1 = result_str
        del result_str
        result_str = ''.join(secrets.choice(letters) for _ in range(64))
        self.key2 = result_str