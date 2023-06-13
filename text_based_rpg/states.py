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

    name: str
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

    def change_name(self, data: dict[str, str]) -> pc.Component:
        if (name := data.get('name')):
            self.name = name.title()
            self.create_session()
            # return pc.html(
            #     f'''
            #     <script>
            #     localStorage.setItem('key1', '{self.key1}');
            #     localStorage.setItem('key2', '{self.key2}');
            #     console.log("Data saved");
            #     </script>
            #     '''
            # )
            return pc.redirect(f'/game?key1={self.key1}&key2={self.key2}')

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
            cursor.close()
        
                


    def generate_new_key_pair(self):
        letters = string.ascii_lowercase
        result_str = ''.join(secrets.choice(letters) for _ in range(64))
        self.key1 = result_str
        del result_str
        result_str = ''.join(secrets.choice(letters) for _ in range(64))
        self.key2 = result_str
        
class LoginState(BaseState):
    def login(self, data: dict[str, str]) -> pc.event.EventSpec:
        if (key1 := data.get('key1')) and len(key1) != 64:
            return pc.window_alert('Error invalid key1')

        if (key2 := data.get('key2')) and len(key2) != 64:
            return pc.window_alert("Error invalid key2")
        return pc.redirect(f'/game/?key1={key1}&key2={key2}')
        

class QueryParamsParsing(BaseState):
    
    key1: str
    key2: str
    def verify_keys_and_cache(self) -> pc.event.EventSpec:
        '''
        The result will be stored in the Self object.\n
        key1: ``self.key1``\n
        key2: ``self.key2``
        '''
        if (result1 := self.get_key1()):
            return result1
        if (result2 := self.get_key2()):
            return result2
    def get_key1(self) -> pc.event.EventSpec:
        if (key1 := self.get_query_params().get('key1')): 
            '''
            Verify it exists
            '''
            with sqlite3.connect("pynecone.db") as connection:
                cursor = connection.cursor()
                cursor.execute("SELECT COUNT(*) FROM users WHERE key1=?;", (key1,))
                count: int = cursor.fetchone()[0]
                cursor.close()
                if count != 0:
                    self.key1 = key1
                    return

                
        return pc.redirect('/start/')
    
    def get_key2(self) -> pc.event.EventSpec:
        if (key2:= self.get_query_params().get('key2')): 
            '''
            Verify it exists
            '''
            with sqlite3.connect("pynecone.db") as connection:
                cursor = connection.cursor()
                cursor.execute("SELECT COUNT(*) FROM users WHERE key2=?;", (key2,))
                count: int = cursor.fetchone()[0]
                cursor.close()
                if count != 0:
                    self.key2 = key2
                    return

                
        return pc.redirect('/start/')
    
    