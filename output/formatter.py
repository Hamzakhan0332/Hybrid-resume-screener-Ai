from pydantic import BaseModel, Field
from typing import List, Optional

class ScreeningResult(BaseModel):
    candidate_name: str
    overall_match: float
    hard_skills_match: float
    semantic_match: float
    soft_skills_match: float
    matched_skills: List[str]
    missing_skills: List[str]
    explanation: str
    confidence_interval: List[float] = Field(default_factory=lambda: [0.0, 100.0])

class BatchResult(BaseModel):
    results: List[ScreeningResult]
    job_description_summary: str
