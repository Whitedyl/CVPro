from typing import Dict
import requests
from os import getenv
from dotenv import load_dotenv
import json
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class JobAnalyzer:
    def __init__(self):
        load_dotenv()
        self.api_key = getenv("HUGGINGFACE_API_KEY")
        if not self.api_key:
            logger.error("Hugging Face API key not found")
            raise ValueError("Hugging Face API key not found")
        self.api_url = "https://api-inference.huggingface.co/models/google/flan-t5-large"
        self.headers = {"Authorization": f"Bearer {self.api_key}"}

    async def analyze_job_description(self, job_text: str) -> Dict:
        logger.info("Starting job description analysis")
        if not job_text:
            logger.error("Empty job text provided")
            return {}

        try:
            prompt = self.create_prompt(job_text)
            logger.info("Calling Hugging Face API...")
            
            response = requests.post(
                self.api_url,
                headers=self.headers,
                json={"inputs": prompt}
            )
            
            if response.status_code != 200:
                logger.error(f"API error: {response.text}")
                return self.basic_extraction(job_text)

            response_text = response.json()[0]['generated_text']
            logger.info(f"Raw response: {response_text}")
            
            parsed_data = self.parse_response(response_text, job_text)
            logger.info("Successfully parsed response")
            return parsed_data
            
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")
            return self.basic_extraction(job_text)

    def create_prompt(self, job_text: str) -> str:
        return f"Extract from this job description: title, required skills, experience level, domain. Job text: {job_text}"

    def parse_response(self, response_text: str, original_text: str) -> Dict:
        lines = original_text.split('\n')
        return {
            "title": self.extract_title(lines),
            "required_skills": self.extract_skills(original_text),
            "experience": self.extract_experience(original_text),
            "domain": self.extract_domain(original_text),
            "description_text": original_text,
            "feedback": response_text
        }

    def extract_title(self, lines: list) -> str:
        """Extract job title from first few lines"""
        for line in lines[:3]:  # Check first 3 lines
            if any(word in line.lower() for word in ['developer', 'engineer', 'manager', 'analyst']):
                return line.strip()
        return lines[0].strip() if lines else ""

    def extract_skills(self, text: str) -> list:
        """Extract required skills from job description"""
        skills = []
        text = text.lower()
        
        # Common skill indicators
        skill_markers = ['requirements:', 'required skills:', 'qualifications:', 'must have:']
        
        for marker in skill_markers:
            if marker in text:
                # Get text after marker until next section
                section = text.split(marker)[1].split('\n\n')[0]
                skills.extend([s.strip() for s in section.split(',') if s.strip()])
                
        return list(set(skills)) if skills else []

    def extract_experience(self, text: str) -> int:
        """Extract years of experience required"""
        text = text.lower()
        try:
            for line in text.split('\n'):
                if any(word in line for word in ['years', 'experience']):
                    numbers = [int(word) for word in line.split() if word.isdigit()]
                    if numbers:
                        return min(numbers)  # Use minimum if multiple numbers found
        except Exception:
            pass
        return 0

    def extract_domain(self, text: str) -> str:
        """Extract primary domain/industry"""
        text = text.lower()
        domains = {
            'software': ['software', 'web', 'application', 'development'],
            'data': ['data', 'analytics', 'machine learning', 'ai'],
            'network': ['network', 'infrastructure', 'cloud', 'devops']
        }
        
        for domain, keywords in domains.items():
            if any(keyword in text for keyword in keywords):
                return domain.title()
                
        return "Technology"  # Default domain

    def basic_extraction(self, job_text: str) -> Dict:
        """Fallback extraction method"""
        lines = job_text.split('\n')
        return {
            "title": lines[0].strip() if lines else "",
            "required_skills": [],
            "experience": 0,
            "domain": "Technology",
            "description_text": job_text,
            "feedback": "Basic extraction used"
        }