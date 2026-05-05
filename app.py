import os
import argparse
import json
from ingest.file_handler import FileHandler
from extract.skill_extractor import SkillExtractor
from extract.jd_parser import JDParser
from match.embedder import Embedder
from match.llm_enhancer import LLMEnhancer
from match.scorer import Scorer
from output.bias_check import Anonymizer
from output.formatter import ScreeningResult

class ResumeScreenerApp:
    def __init__(self):
        print("Initializing AI Modules... (this may take a moment)")
        self.file_handler = FileHandler()
        self.skill_extractor = SkillExtractor()
        self.jd_parser = JDParser(self.skill_extractor)
        self.embedder = Embedder()
        self.llm_enhancer = LLMEnhancer()
        self.scorer = Scorer()
        self.anonymizer = Anonymizer()

    def screen(self, resume_path: str, jd_text: str) -> ScreeningResult:
        # 1. Parse Resume
        resume_data = self.file_handler.process(resume_path)
        raw_resume_text = resume_data.get("raw_text", "")
        
        # 2. Anonymize for bias mitigation
        clean_resume_text = self.anonymizer.anonymize(raw_resume_text)
        
        # 3. Extract Skills
        resume_skills = self.skill_extractor.extract_skills(clean_resume_text)
        jd_data = self.jd_parser.parse(jd_text)
        jd_skills = set(jd_data["required_skills"])
        
        # 4. Semantic Matching
        resume_emb = self.embedder.encode(clean_resume_text)
        jd_emb = self.embedder.encode(jd_text)
        similarity = float(self.embedder.compute_similarity(resume_emb, jd_emb)[0][0])
        
        # 5. LLM Enhancement (Soft Skills)
        llm_results = self.llm_enhancer.get_soft_skill_score(clean_resume_text, jd_text)
        
        # 6. Scoring
        hard_skill_results = self.scorer.calculate_score(resume_skills, jd_skills)
        final_results = self.scorer.fuse_scores(hard_skill_results, similarity, llm_results)
        
        return ScreeningResult(
            candidate_name=os.path.basename(resume_path),
            overall_match=final_results["overall_match"],
            hard_skills_match=final_results["hard_skills_match"],
            semantic_match=final_results["semantic_match"],
            soft_skills_match=final_results["soft_skills_match"],
            matched_skills=hard_skill_results["matched_skills"],
            missing_skills=hard_skill_results["missing_skills"],
            explanation=final_results["explanation"]
        )

def main():
    parser = argparse.ArgumentParser(description="Hybrid Resume Screener AI CLI")
    parser.add_argument("--resume", type=str, help="Path to resume file")
    parser.add_argument("--jd", type=str, help="Path to job description file")
    args = parser.parse_args()

    if not args.resume or not args.jd:
        print("Usage: python app.py --resume path/to/cv.pdf --jd path/to/jd.txt")
        return

    app = ResumeScreenerApp()
    
    with open(args.jd, 'r', encoding='utf-8') as f:
        jd_content = f.read()
    
    result = app.screen(args.resume, jd_content)
    print("\n--- Screening Result ---")
    print(json.dumps(result.dict(), indent=2))

if __name__ == "__main__":
    main()
