"""Welcome to Pynecone! This file outlines the steps to create a basic app."""
import pynecone as pc


from .states import *


@pc.route('/game/', on_load=QueryParamsParsing.verify_keys_and_cache)
def game() -> pc.Component:
    

    return pc.center(
        pc.vstack(
            pc.text("1 is " + QueryParamsParsing.key1),
            pc.text("2 is " + QueryParamsParsing.key2),
            pc.stack(
                pc.foreach(LoggingState.logs, lambda item: pc.text(item)),
                width="55%",
                bg="#AAAAAA",
                padding="8px",
                border_radius="4px",
            ),
            pc.hstack(
                pc.foreach(LoggingState.options, lambda x: pc.button(x,
                                                                           on_click=lambda: LoggingState.use_option(x)))
            ),
            width="100%"
        ),
        width="100%"
    )
def start_game() -> pc.Component:
    return pc.stack(

        pc.center(
            pc.form(

            pc.input(

                id='name',
                placeholder="Your name",

            ),

            on_submit=UserInformation.change_name,

        )

        ),
    )

def page404() -> pc.Component:
    return pc.center(
        pc.heading(pc.link("This page does not exist(404)", href='https://youtu.be/xvFZjo5PgG0'))
        )


# Add state and page to the app.
app = pc.App(state=BaseState)


app.add_page(start_game, '/start/')

app.add_page(start_game, '/')

app.add_custom_404_page(page404)
app.compile()
