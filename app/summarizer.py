from transformers import pipeline
from pdfminer.high_level import extract_text
from io import BytesIO
import requests
import textwrap
from keybert import KeyBERT
from textblob import TextBlob

# Initialize models
summarizer = pipeline("summarization", model="t5-small", tokenizer="t5-small")
keyword_model = KeyBERT()

# Helper: Split long text into chunks
def chunk_text(text, max_words=400):
    words = text.split()
    return [" ".join(words[i:i+max_words]) for i in range(0, len(words), max_words)]

def process_document(file_url):
    res = requests.get(file_url)
    text = extract_text(BytesIO(res.content))

    # Step 1: Chunk the text
    chunks = chunk_text(text)

    # Step 2: Summarize each chunk
    summaries = []
    for chunk in chunks:
        summary = summarizer(chunk, max_length=100, min_length=20, do_sample=False)[0]["summary_text"]
        summaries.append(summary)

    # Step 3: Combine all summaries into a final summary
    final_summary = " ".join(summaries)

    # Step 4: Sentiment analysis (on full text)
    sentiment_score = TextBlob(text).sentiment.polarity
    sentiment = "positive" if sentiment_score > 0 else "negative"

    # Step 5: Extract keywords
    keywords = keyword_model.extract_keywords(text, top_n=5)
    keyword_list = [kw[0] for kw in keywords]

    return {
        "summary": final_summary,
        "sentiment": sentiment,
        "keywords": keyword_list,
    }