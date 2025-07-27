from transformers import pipeline
from pdfminer.high_level import extract_text
from io import BytesIO
import requests
from keybert import KeyBERT
from textblob import TextBlob

# Initialize models
summarizer = pipeline("summarization", model="t5-small", tokenizer="t5-small")
keyword_model = KeyBERT()

def chunk_text(text, max_words=400):
    words = text.split()
    return [" ".join(words[i:i + max_words]) for i in range(0, len(words), max_words)]

def process_document(file_url):
    try:
        res = requests.get(file_url)
        if res.status_code != 200:
            print(f"❌ Failed to download file. Status code: {res.status_code}")
            return None

        print(f"📄 Downloaded file from {file_url} (size: {len(res.content)} bytes)")

        try:
            text = extract_text(BytesIO(res.content))
        except Exception as e:
            print(f"❌ Failed to extract PDF text: {e}")
            return None

        if not text or len(text.strip()) < 20:
            print("⚠️ Extracted text is too short or empty.")
            return None

        print("✅ Successfully extracted PDF text.")

        # Chunking
        chunks = chunk_text(text)
        summaries = []

        for chunk in chunks:
            summary = summarizer(chunk, max_length=100, min_length=20, do_sample=False)[0]["summary_text"]
            summaries.append(summary)

        final_summary = " ".join(summaries)

        # Sentiment
        sentiment_score = TextBlob(text).sentiment.polarity
        sentiment = "positive" if sentiment_score > 0 else "negative"

        # Keywords
        keywords = keyword_model.extract_keywords(text, top_n=5)
        keyword_list = [kw[0] for kw in keywords]

        return {
            "summary": final_summary,
            "sentiment": sentiment,
            "keywords": keyword_list,
        }

    except Exception as e:
        print(f"❌ Unexpected error in process_document: {e}")
        return None