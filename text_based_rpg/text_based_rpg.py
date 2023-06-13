import pynecone as pc


from .states import *

def loginByKeys() -> pc.Component:
    return pc.stack(
        pc.center(
        pc.heading(f"Welcome to text-based-rpg!")),
        
        pc.center(

        pc.form(
            pc.input(
                placeholder='key1',
                id='key1',
                type_='password'
                ),
            pc.input(
                placeholder='key2',
                id='key2',
                type_='password'
            ),
            pc.button('Login', type_='submit',
                _hover={
                    'bg': 'lightgreen'
                    
                    
                }
                      ),
            
            pc.text("New here? ", pc.link("Start your adventure!", href='/start/')),
            on_submit=LoginState.login

        ),
        
    ))
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
            pc.heading('Welcome user', margin_bottom='10%'),

            pc.input(

                id='name',
                placeholder="Your name",
                margin_bottom='10%'
            ),
            pc.button(
                'Start the adventure!',
                type_='submit',
                _hover={
                    'bg': 'lightgreen'
                    
                    
                }
            ),
            pc.text("Already an adventurer? ", pc.link("Log in back", href='/login/')),
            on_submit=UserInformation.change_name,

        )

        ),
    )

def page404() -> pc.Component:
    return pc.center(
        pc.heading(pc.link("This page does not exist(404)", href='https://youtu.be/xvFZjo5PgG0'))
        )


app = pc.App(state=BaseState,)

app.add_page(start_game, '/start/')

app.add_page(loginByKeys, '/')

app.add_page(loginByKeys, '/login/')

app.add_custom_404_page(page404)
app.compile()
