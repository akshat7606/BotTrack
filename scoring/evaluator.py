from sentence_transformers import SentenceTransformer, util

model = SentenceTransformer("all-MiniLM-L6-v2")

def evaluate_session(session):
    messages = session.get("messages", [])
    user_messages = [msg["message"].lower() for msg in messages if msg["sender"] == "user"]

    # Short session with only one user message — assume not helpful
    if len(user_messages) == 1:
        return "failure"

    # Sentiment-based quick classification
    negative_phrases = ["not satisfied", "dislike", "this didn’t help", "this is useless", "no help", "waste of time"]
    positive_phrases = ["thank you", "thanks", "this helped", "great", "awesome", "perfect", "got it"]

    if any(neg in msg for msg in user_messages for neg in negative_phrases):
        return "failure"
    if any(pos in msg for msg in user_messages for pos in positive_phrases):
        return "success"

    # Rephrasing check
    embeddings = model.encode(user_messages, convert_to_tensor=True)
    similarities = util.cos_sim(embeddings, embeddings)

    rephrase_count = 0
    for i in range(len(user_messages)):
        for j in range(i + 1, len(user_messages)):
            if similarities[i][j] > 0.8:
                rephrase_count += 1

    if rephrase_count >= 2:
        return "failure"

    return "success"
