"""Welcome to Pynecone! This file outlines the steps to create a basic app."""
from pcconfig import config

import pynecone as pc



class State(pc.State):
    ...


def index() -> pc.Component:
    return pc.center(
        pc.button("Toggle mode",pc.icon(tag="moon"), on_click=pc.toggle_color_mode)
    )


# Add state and page to the app.
app = pc.App(state=State)
app.add_page(index)
app.compile()
