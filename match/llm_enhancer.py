import os
from typing import Dict, Any, List
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

class LLMEnhancer:
    def __init__(self):
        self.provider = os.getenv("LLM_PROVIDER", "groq").lower()
        self.groq_key = os.getenv("GROQ_API_KEY")
        self.openai_key = os.getenv("OPENAI_API_KEY")
        self.client = None

        if self.provider == "groq" and self.groq_key:
            from groq import Groq
            self.client = Groq(api_key=self.groq_key)
        elif self.provider == "openai" and self.openai_key:
            from openai import OpenAI
            self.client = OpenAI(api_key=self.openai_key)


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
            model = "llama-3.1-8b-instant" if self.provider == "groq" else "gpt-4o-mini"
            
            chat_completion = self.client.chat.completions.create(

                messages=[{"role": "user", "content": prompt}],
                model=model,
                response_format={"type": "json_object"}
            )
            import json
            return json.loads(chat_completion.choices[0].message.content)
        except Exception as e:
            return {"score": 50, "explanation": f"LLM Error ({self.provider}): {str(e)}"}

