from typing import Dict, List, Set
from .skill_extractor import SkillExtractor

class JDParser:
    def __init__(self, extractor: SkillExtractor):
        self.extractor = extractor

    def parse(self, jd_text: str) -> Dict[str, Any]:
        """Parses job description into structured data."""
        # In production, use an LLM to distinguish between 'required' and 'preferred'
        # For this version, we'll extract all identifiable skills.
        
        extracted_skills = self.extractor.extract_skills(jd_text)
        normalized_skills = self.extractor.normalize_skills(extracted_skills)
        
        # Simple heuristic for experience years: look for "X+ years" or "X years"
        # (This could be improved with regex or LLM)
        
        return {
            "required_skills": list(normalized_skills),
            "raw_text": jd_text,
            "summary": jd_text[:200] + "..." # Placeholder for actual summary
        }
