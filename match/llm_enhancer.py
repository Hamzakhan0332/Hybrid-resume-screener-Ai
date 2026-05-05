import os
from typing import Dict, Any, List
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

class LLMEnhancer:
    def __init__(self):
        self.api_key = os.getenv("GROQ_API_KEY")
        self.provider = os.getenv("LLM_PROVIDER", "groq")
        
        if self.api_key and self.provider == "groq":
            self.client = Groq(api_key=self.api_key)
        else:
            self.client = None

    def get_soft_skill_score(self, resume_text: str, jd_text: str) -> Dict[str, Any]:
        """Uses LLM to evaluate soft skills and provide an explanation."""
        if not self.client:
            return {"score": 50, "explanation": "LLM not configured (missing API key)."}

        prompt = f"""
        Compare the following Resume and Job Description.
        Focus on soft skills (leadership, communication, team work) and overall cultural fit.
        
        Job Description:
        {jd_text[:1000]}
        
        Resume:
        {resume_text[:2000]}
        
        Output a JSON only with:
        - "score": 0-100
        - "explanation": a concise 2-sentence summary of the match.
        """

        try:
            chat_completion = self.client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model="llama-3-8b-8192",
                response_format={"type": "json_object"}
            )
            import json
            return json.loads(chat_completion.choices[0].message.content)
        except Exception as e:
            return {"score": 50, "explanation": f"LLM Error: {str(e)}"}
