from dotenv import dotenv_values

_config = dotenv_values(".env")

DB_CONNECTION_URL = _config["DATABASE_URL"]
TOKEN = _config["BOT_TOKEN"]
CATEGORY = int(_config["CATEGORY"])
