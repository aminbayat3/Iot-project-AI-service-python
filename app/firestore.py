import firebase_admin
from firebase_admin import credentials, firestore
from app.config import Config 

cred = credentials.Certificate(Config.GOOGLE_APPLICATION_CREDENTIALS)
firebase_admin.initialize_app(cred)

db = firestore.client()