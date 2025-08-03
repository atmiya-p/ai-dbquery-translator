import spacy
import datetime

# pre trained english language model - en_core_web_sm
nlp = spacy.load("en_core_web_sm")

def parse_nl(query):
    doc_object = nlp(query.lower())

    entities = {"date": None, "person": None, "product": None}

    # https://spacy.io/api/entityrecognizer
    for entity in doc_object.ents:
        if entity.label_ == "DATE":
            entities["date"] = entity.text
        elif entity.label_ == "PERSON":
            entities["person"] = entity.text
            
