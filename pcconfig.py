import pynecone as pc

class TextbasedrpgConfig(pc.Config):
    pass

config = TextbasedrpgConfig(
    app_name="text_based_rpg",
    db_url="sqlite:///pynecone.db",
    env=pc.Env.DEV,
)