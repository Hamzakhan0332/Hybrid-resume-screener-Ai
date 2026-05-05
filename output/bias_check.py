import re
from typing import List

class Anonymizer:
    def __init__(self):
        # Very basic regex patterns for anonymization
        # In production, use spaCy NER to find PERSON, GPE, etc.
        self.email_pattern = r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+'
        self.phone_pattern = r'\b(?:\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}\b'

    def anonymize(self, text: str) -> str:
        """Removes sensitive info like email and phone."""
        text = re.sub(self.email_pattern, "[EMAIL REDACTED]", text)
        text = re.sub(self.phone_pattern, "[PHONE REDACTED]", text)
        return text

    def remove_bias_proxies(self, text: str) -> str:
        """Placeholder for removing gender pronouns or age indicators."""
        proxies = ["Mr\.", "Ms\.", "Mrs\.", "He ", "She ", "Him ", "Her ", "born in"]
        for proxy in proxies:
            text = re.compile(proxy, re.IGNORECASE).sub("[REDACTED] ", text)
        return text
