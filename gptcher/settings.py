import os
from dotenv import load_dotenv

load_dotenv(override=True)


is_prod = os.getenv("IS_PROD") == "True"
if is_prod:
    print("Running in production mode")
    token = os.getenv("TELEGRAM_TOKEN_PROD")
    table_prefix = ""
else:
    print("Running in development mode")
    token = os.getenv("TELEGRAM_TOKEN_DEV")
    table_prefix = "dev_"