from app.summarizer import process_document
from firebase_admin import firestore
from app.firestore import db
from datetime import datetime

def handle_document_upload(data):
    file_id = data.get("fileId")
    file_url = data.get("fileUrl")

    if not file_id or not file_url:
        print("❌ Invalid message data, missing fileId or fileUrl.")
        return

    result = process_document(file_url)

    doc_ref = db.collection("documents").document(file_id)
    doc_snapshot = doc_ref.get()

    if not doc_snapshot.exists:
        print(f"⚠️ Document with ID {file_id} not found in Firestore. Skipping update.")
        return

    if not result:
        print("⚠️ Skipping document update due to processing error.")
        doc_ref.update({
            "status": "failed",
            "error": "File not accessible or unreadable",
            "completedAt": firestore.SERVER_TIMESTAMP
        })
        return

    # Only update Firestore if summarization was successful
    doc_ref.update({
        **result,
        "status": "completed",
        "completedAt": firestore.SERVER_TIMESTAMP
    })
    print(f"✅ Document {file_id} updated successfully.")
