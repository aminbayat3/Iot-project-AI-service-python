# 🤖 AI Processing Service

A Python-based AI processing service deployed on **Google Kubernetes Engine (GKE)** for scalable document analysis.  
The service retrieves documents from Google Cloud Storage (GCS) via signed URLs, processes them with AI models, and updates results in Firestore.

---

## ✨ Features

- **⚡ Auto-scaling** — GKE automatically adjusts instances based on load
- **⚖ Load balancing** — Evenly distributes tasks across service instances
- **📄 File Retrieval** — Securely downloads documents via short-lived signed URLs
- **🔄 Preprocessing** — Splits large PDFs for processing with the T5-small model
- **🧠 AI Computations**:
  - Summarization (**T5-small**)
  - Sentiment Analysis
  - Keyword Extraction
- **📝 Result Merging** — Reassembles chunk summaries into a complete summary
- **📌 Metadata Update** — Writes results and status updates back to Firestore
- **📬 Pub/Sub Integration** — Listens for file upload events via Google Cloud Pub/Sub

---

## 🛠 Tech Stack

**Language**: Python 3.10  
**AI / NLP**:
- transformers (T5-small)
- torch
- nltk
- keybert
- textblob

**Google Cloud**:
- google-cloud-pubsub
- firebase-admin
- Google Cloud Storage (GCS)
- Firestore

**PDF Parsing**:
- pdfminer.six

**Environment Management**:
- python-dotenv

---

## 📦 Installation & Local Development

### 1️⃣ Clone the repository
git clone https://github.com/yourusername/ai-processing-service.git
cd ai-processing-service

🖥️ Running Locally
1️⃣ Create a Virtual Environment
python3 -m venv venv
# Activate the environment
source venv/bin/activate      
venv\Scripts\activate         
2️⃣ Install Dependencies
pip install -r requirements.txt
3️⃣ Set Up Environment Variables
Create a .env file in the project root:
GOOGLE_CLOUD_PROJECT=your-gcp-project-id
SUBSCRIPTION_NAME=your-pubsub-subscription-name
GOOGLE_APPLICATION_CREDENTIALS=/path/to/service-account.json
Note: The path for GOOGLE_APPLICATION_CREDENTIALS should be absolute.

4️⃣ Run the Service
python main.py
When running, the service will:

Connect to the specified Pub/Sub subscription

Wait for messages containing signed URLs and metadata

Process documents

Update Firestore

🐳 Running with Docker
1️⃣ Build the Docker Image
docker build -t ai-processing-service .
2️⃣ Run the Container
docker run --env-file .env ai-processing-service
Tip: Make sure your .env file contains valid credentials and file paths.

🚀 Deployment on Google Kubernetes Engine (GKE)
1️⃣ Build and Push the Image to Google Container Registry (GCR)
docker build -t gcr.io/your-gcp-project-id/ai-processing-service:latest .
docker push gcr.io/your-gcp-project-id/ai-processing-service:latest
2️⃣ Deploy to GKE
kubectl apply -f k8s/deployment.yaml

