import os
from dotenv import load_dotenv

load_dotenv()

REQUIRED_ENV_VARS = ["SUBSCRIPTION_NAME","GOOGLE_APPLICATION_CREDENTIALS", "GOOGLE_CLOUD_PROJECT"]

for key in REQUIRED_ENV_VARS:
    if not os.getenv(key):
        raise RuntimeError(f"Missing required environment variable: {key}")

class Config:
    SUBSCRIPTION_NAME = os.getenv("SUBSCRIPTION_NAME")
    GOOGLE_APPLICATION_CREDENTIALS = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
    GOOGLE_CLOUD_PROJECT = os.getenv("GOOGLE_CLOUD_PROJECT")