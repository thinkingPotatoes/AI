from keybert import KeyBERT
from kiwipiepy import Kiwi
from transformers import BertModel

def extractKeywords(text):
    # Check Stopwords
    f = open("stopword.txt", 'r', encoding='utf-8')
    lines = f.readlines()
    stopwords = []
    for line in lines:
        line = line.strip()
        stopwords.append(line)
    f.close()

    # Extract Noun (by. Kiwi)
    kiwi = Kiwi()
    for sentence in kiwi.analyze(text):
        nouns = [token.form for token in sentence[0] if token.tag.startswith('NN') and token.form not in stopwords]
    clean_text = ' '.join(nouns)

    # Extract keywords (by. keybert)
    model = BertModel.from_pretrained('skt/kobert-base-v1')
    kw_model = KeyBERT(model)
    keywords = kw_model.extract_keywords(clean_text, keyphrase_ngram_range=(1, 1), stop_words=None, use_mmr=True, top_n=15)

    result = [keyword[0] for keyword in keywords][:3]
    return result
