from os import environ

env = environ.get("ENVIRONMENT")
if env == "DEV":
    from dotenv import load_dotenv

    load_dotenv()
