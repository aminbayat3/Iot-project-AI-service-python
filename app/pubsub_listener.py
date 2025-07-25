from google.cloud import pubsub_v1
import json
from app.document_handler import handle_document_upload
from app.config import Config 

def listen_for_messages():
    subscriber = pubsub_v1.SubscriberClient()
    
    subscription_path = subscriber.subscription_path(
        Config.GOOGLE_CLOUD_PROJECT,
        Config.SUBSCRIPTION_NAME
    )

    def callback(message):
        try:
            data = json.loads(message.data.decode("utf-8"))
            print("📥 Received message:", data)
            handle_document_upload(data)
            message.ack()
        except Exception as e:
            print("❌ Error handling message:", e)
            message.nack()

    subscriber.subscribe(subscription_path, callback=callback)
    print(f"✅ Listening for messages on: {subscription_path}...")