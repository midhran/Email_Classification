import re
import spacy.cli

# Ensure the model downloads if not present
spacy.cli.download("en_core_web_sm")
import spacy

class PIIMasker:
    def __init__(self):
        self.nlp = spacy.load("en_core_web_sm")
        self.regex_patterns = {
            "email": r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}",
            "phone_number": r"\+?\d[\d\s\-\(\)]{7,}\d",
            "dob": r"\b\d{2}[/-]\d{2}[/-]\d{4}\b",
            "aadhar_num": r"\b\d{4}\s\d{4}\s\d{4}\b",
            "credit_debit_no": r"\b(?:\d[ -]*?){13,16}\b",
            "expiry_no": r"\b(0[1-9]|1[0-2])\/?([0-9]{2})\b"
        }
        self.whitelist = {"MacBook Pro", "Apple", "Norton", "Windows"}

    def mask(self, text: str):
        masked_text = text
        entities = []

        # Regex masking
        for label, pattern in self.regex_patterns.items():
            for match in re.finditer(pattern, masked_text):
                start, end = match.span()
                entity = match.group()
                entities.append({
                    "position": [start, end],
                    "classification": label,
                    "entity": entity
                })
                masked_text = masked_text.replace(entity, f"[{label}]", 1)

        # SpaCy NER for full names
        doc = self.nlp(masked_text)
        for ent in doc.ents:
            if ent.label_ == "PERSON" and ent.text not in self.whitelist:
                start, end = ent.start_char, ent.end_char
                entity = ent.text
                entities.append({
                    "position": [start, end],
                    "classification": "full_name",
                    "entity": entity
                })
                masked_text = masked_text.replace(entity, "[full_name]", 1)

        return masked_text, entities
