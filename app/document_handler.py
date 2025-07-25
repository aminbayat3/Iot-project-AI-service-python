from app.summarizer import process_document
from app.firestore import db
from datetime import datetime

def handle_document_upload(data):
    file_id = data["fileId"]
    file_url = data["fileUrl"]

    result = process_document(file_url)

    db.collection("documents").document(file_id).update({
        **result,
        "status": "completed",
        "completedAt": datetime.utcnow().isoformat()
    })