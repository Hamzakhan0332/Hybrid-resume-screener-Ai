import spacy
from spacy.matcher import PhraseMatcher
from typing import List, Set
import os

class SkillExtractor:
    def __init__(self, model_name: str = "en_core_web_md"):
        try:
            self.nlp = spacy.load(model_name)
        except OSError:
            # Fallback if model not found, instruction will be given to download it
            print(f"Model {model_name} not found. Please run 'python -m spacy download {model_name}'")
            self.nlp = spacy.blank("en")
        
        self.matcher = PhraseMatcher(self.nlp.vocab)
        self.skills_list = self._load_default_skills()
        self._add_skills_to_matcher(self.skills_list)

    def _load_default_skills(self) -> List[str]:
        # A basic set of common skills. In production, this would be a large CSV/JSON.
        return [
            "Python", "Java", "C++", "JavaScript", "React", "Node.js", "SQL", "PostgreSQL",
            "AWS", "GCP", "Azure", "Docker", "Kubernetes", "Machine Learning", "Deep Learning",
            "Data Analysis", "Project Management", "Agile", "Scrum", "Git", "DevOps",
            "CI/CD", "TensorFlow", "PyTorch", "NLP", "Computer Vision", "HTML", "CSS",
            "TypeScript", "Flask", "Django", "FastAPI", "Pandas", "NumPy", "Spark"
        ]

    def _add_skills_to_matcher(self, skills: List[str]):
        patterns = [self.nlp.make_doc(text) for text in skills]
        self.matcher.add("SKILL", patterns)

    def extract_skills(self, text: str) -> Set[str]:
        """Extracts skills using spaCy NER and PhraseMatcher."""
        doc = self.nlp(text)
        found_skills = set()

        # 1. Using PhraseMatcher (Exact/Case-insensitive matches)
        matches = self.matcher(doc)
        for match_id, start, end in matches:
            span = doc[start:end]
            found_skills.add(span.text.strip())

        # 2. Using custom NER (in production, we'd train a model)
        # For now, we'll just look for ORG/PRODUCT if they might be skills
        for ent in doc.ents:
            if ent.label_ in ["ORG", "PRODUCT"] and ent.text in self.skills_list:
                found_skills.add(ent.text)

        return found_skills

    def normalize_skills(self, skills: Set[str]) -> Set[str]:
        """Normalizes skill names (e.g., 'python' -> 'Python')."""
        # Simple implementation: match against the original skills_list
        normalized = set()
        skill_map = {s.lower(): s for s in self.skills_list}
        
        for s in skills:
            if s.lower() in skill_map:
                normalized.add(skill_map[s.lower()])
            else:
                normalized.add(s) # Keep as is if not in list
        
        return normalized

if __name__ == "__main__":
    extractor = SkillExtractor()
    text = "Experienced Python developer with skills in React and AWS. Familiar with machine learning and PostgreSQL."
    print(extractor.extract_skills(text))
