from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline
from keybert import KeyBERT
import torch

print("Loading summarization model...")
tokenizer = AutoTokenizer.from_pretrained("facebook/bart-large-cnn")
model = AutoModelForSeq2SeqLM.from_pretrained("facebook/bart-large-cnn")

print("Loading sentiment model...")
sentiment_analyzer = pipeline("sentiment-analysis",
                              model="distilbert-base-uncased-finetuned-sst-2-english")

print("Loading keyword model...")
keyword_model = KeyBERT()

print("All models loaded! ✅")


def summarize_email(text):
    if len(text.split()) < 30:
        return "⚠️ Text too short. Please paste a longer email."
    inputs = tokenizer(text, return_tensors="pt", max_length=1024, truncation=True)
    summary_ids = model.generate(inputs["input_ids"], max_length=130, min_length=30)
    return tokenizer.decode(summary_ids[0], skip_special_tokens=True)


def extract_keywords(text):
    keywords = keyword_model.extract_keywords(text, top_n=5)
    return [word for word, score in keywords]


def detect_sentiment(text):
    result = sentiment_analyzer(text[:500])
    label = result[0]['label']
    score = result[0]['score']
    if label == "POSITIVE":
        return f"😊 Positive ({score:.0%} confidence)"
    else:
        return f"😟 Negative ({score:.0%} confidence)"


def detect_action_items(text):
    action_keywords = [
        "please", "kindly", "reply", "respond", "send", "submit",
        "deadline", "by tomorrow", "urgent", "asap", "review",
        "confirm", "let me know", "follow up", "attach"
    ]
    sentences = text.split('.')
    action_items = []
    for sentence in sentences:
        if any(keyword in sentence.lower() for keyword in action_keywords):
            clean = sentence.strip()
            if clean:
                action_items.append(f"• {clean}")
    if action_items:
        return "\n".join(action_items[:5])
    return "No action items detected."