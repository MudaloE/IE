import spacy

nlp = spacy.load("en_core_web_sm")

def evaluate_response(transcription):
    doc = nlp(transcription)
    word_count = len([token.text for token in doc if token.is_alpha])
    score = {
        "fluency": min(word_count / 100, 9),
        "grammar": min(len([sent for sent in doc.sents]) / 5, 9),
        "vocabulary": min(len(set([token.text for token in doc])) / 50, 9),
        "pronunciation": 8  # Placeholder for detailed scoring
    }
    return score