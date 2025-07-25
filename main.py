from dotenv import load_dotenv
from app.pubsub_listener import listen_for_messages

if __name__ == "__main__":
    load_dotenv()
    listen_for_messages()