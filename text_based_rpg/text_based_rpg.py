"""Welcome to Pynecone! This file outlines the steps to create a basic app."""
from pcconfig import config
import random
import string
import pynecone as pc
from typing import List

docs_url = "https://pynecone.io/docs/getting-started/introduction"
filename = f"{config.app_name}/{config.app_name}.py"


class State(pc.State):
    """The app state."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.generate_new_key_pair()
        self.options = ['a', 'b']
        self.logs += ['hi', 'it works!']

    """keys part
    a user has two keys, consisting of 64 bits of random nonsense,
    with which the user can be identified in the database.
    """
    key1: str
    key2: str

    options: List[str]
    selected_option: str

    logs: List[str]

    def generate_new_key_pair(self):
        letters = string.ascii_lowercase
        result_str = ''.join(random.choice(letters) for _ in range(64))
        self.key1 = result_str
        del result_str
        result_str = ''.join(random.choice(letters) for _ in range(64))
        self.key2 = result_str

    def use_option(self, option):
        if option not in self.options: raise "option not in self.options!"
        self.logs.append(f"used option {option}.")


def render_log_item(log_item):
    return pc.text(log_item)


def index() -> pc.Component:
    return pc.center(
        pc.vstack(
            pc.text("1 is " + State.key1),
            pc.text("2 is " + State.key2),
            pc.stack(
                pc.foreach(State.logs, render_log_item),
                width="55%",
                bg="#AAAAAA",
                padding="8px",
                border_radius="4px",
            ),
            pc.hstack(
                pc.foreach(State.options, lambda x: pc.button(x, on_click=lambda _: State.use_option(x)))
            ),
            width="100%"
        ),
        width="100%"
    )


# Add state and page to the app.
app = pc.App(state=State)
app.add_page(index)
app.compile()
