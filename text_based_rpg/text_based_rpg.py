"""Welcome to Pynecone! This file outlines the steps to create a basic app."""
import  secrets
import string
import pynecone as pc



class BaseState(pc.State):
    '''
    Represents the BaseState, this makes it possible in the future to create multiple States.
    Inherit from BaseState
    '''
    ...
class KeyGenerationState(BaseState):

    """
    keys part
    a user has two keys, consisting of 64 bits of random nonsense,
    with which the user can be identified in the database.
    """
    key1: str
    key2: str

    options: list[str]
    selected_option: str

    logs: list[str]
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.generate_new_key_pair()
        self.options = ['a', 'b']
        self.logs += ['hi', 'it works!']


    def generate_new_key_pair(self):
        letters = string.ascii_lowercase
        result_str = ''.join(secrets.choice(letters) for _ in range(64))
        self.key1 = result_str
        del result_str
        result_str = ''.join(secrets.choice(letters) for _ in range(64))
        self.key2 = result_str

    def use_option(self, option):
        if option not in self.options: raise "option not in self.options!"
        self.logs.append(f"used option {option}.")




def index() -> pc.Component:
    return pc.center(
        pc.vstack(
            pc.text("1 is " + KeyGenerationState.key1),
            pc.text("2 is " + KeyGenerationState.key2),
            pc.stack(
                pc.foreach(KeyGenerationState.logs, lambda item: pc.text(item)),
                width="55%",
                bg="#AAAAAA",
                padding="8px",
                border_radius="4px",
            ),
            pc.hstack(
                pc.foreach(KeyGenerationState.options, lambda x: pc.button(x,
                                                                           on_click=lambda: KeyGenerationState.use_option(x)))
            ),
            width="100%"
        ),
        width="100%"
    )


# Add state and page to the app.
app = pc.App(state=BaseState)
app.add_page(index)
app.compile()
