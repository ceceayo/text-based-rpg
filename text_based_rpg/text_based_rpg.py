"""Welcome to Pynecone! This file outlines the steps to create a basic app."""
from pcconfig import config
import random
import string
import pynecone as pc

docs_url = "https://pynecone.io/docs/getting-started/introduction"
filename = f"{config.app_name}/{config.app_name}.py"


class State(pc.State):
    """The app state."""

    """keys part
    a user has two keys, consisting of 64 bits of random nonsense,
    with which the user can be identified in the database.
    """
    key1: str
    key2: str

    def generate_new_key_pair(self):
        letters = string.ascii_lowercase
        result_str = ''.join(random.choice(letters) for _ in range(64))
        self.key1 = result_str
        del result_str
        result_str = ''.join(random.choice(letters) for _ in range(64))
        self.key2 = result_str

    pass


def index() -> pc.Component:
    return pc.center(
        pc.text("hi")
    )


# Add state and page to the app.
app = pc.App(state=State)
app.add_page(index)
app.compile()
