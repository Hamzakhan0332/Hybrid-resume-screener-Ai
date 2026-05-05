from typing import Dict, Any, List, Set
import numpy as np

class Scorer:
    def __init__(self):
        pass

    def calculate_score(self, resume_skills: Set[str], jd_skills: Set[str]) -> Dict[str, Any]:
        """Calculates a match score based on skill overlap."""
        if not jd_skills:
            return {"overall_score": 0, "matched": [], "missing": []}

        matched = resume_skills.intersection(jd_skills)
        missing = jd_skills - resume_skills
        
        # Simple percentage match
        match_percentage = (len(matched) / len(jd_skills)) * 100
        
        return {
            "overall_score": round(match_percentage, 2),
            "matched_skills": list(matched),
            "missing_skills": list(missing)
        }

    def fuse_scores(self, hard_skill_results: Dict[str, Any], semantic_score: float, llm_results: Dict[str, Any]) -> Dict[str, Any]:
        """Fuses multiple scores into a final weighted score."""
        # Weights: Hard Skills (40%), Semantic Similarity (40%), LLM Soft Skills (20%)
        
        hard_score = hard_skill_results["overall_score"]
        soft_score = llm_results.get("score", 50)
        semantic_percentage = semantic_score * 100
        
        final_score = (hard_score * 0.4) + (semantic_percentage * 0.4) + (soft_score * 0.2)
        
        return {
            "overall_match": round(final_score, 1),
            "hard_skills_match": round(hard_score, 1),
            "semantic_match": round(semantic_percentage, 1),
            "soft_skills_match": round(soft_score, 1),
            "explanation": llm_results.get("explanation", "Match based on skill extraction and semantic similarity.")
        }
