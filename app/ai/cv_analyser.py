from typing import Dict
import requests
from os import getenv
from dotenv import load_dotenv
import json
import logging
import re

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CVAnalyzer:
    def __init__(self):
        load_dotenv()
        self.api_key = getenv("HUGGINGFACE_API_KEY")
        if not self.api_key:
            logger.error("Hugging Face API key not found")
            raise ValueError("Hugging Face API key not found")
        self.api_url = "https://api-inference.huggingface.co/models/google/flan-t5-large"
        self.headers = {"Authorization": f"Bearer {self.api_key}"}

    async def analyze_cv(self, cv_text: str) -> Dict:
        """Main analysis method"""
        logger.info("Starting CV analysis")
        if not cv_text:
            logger.error("Empty CV text provided")
            return {}

        try:
            # Extract data using regex first
            extracted_data = self.extract_data(cv_text)
            
            # Create a more specific prompt for better feedback
            prompt = f"""Analyze this CV and provide specific feedback in these areas:
            1. Skills matching for technology roles
            2. Education relevance
            3. Experience presentation
            4. Overall CV structure
            
            CV Details:
            Name: {extracted_data['name']}
            Skills: {', '.join(extracted_data['skills'])}
            Education: {', '.join(extracted_data['education'])}
            Experience: {extracted_data['experience']} years
            
            Provide constructive feedback in 3-4 sentences."""

            response = requests.post(
                self.api_url,
                headers=self.headers,
                json={"inputs": prompt}
            )
            
            if response.status_code == 200:
                feedback = response.json()[0]['generated_text']
                if not feedback or feedback.isspace():
                    feedback = self.generate_basic_feedback(extracted_data)
            else:
                feedback = self.generate_basic_feedback(extracted_data)

            # Add feedback to extracted data
            extracted_data["feedback"] = feedback
            return extracted_data
            
        except Exception as e:
            logger.error(f"Error in analysis: {str(e)}")
            return self.basic_extraction(cv_text)

    def generate_basic_feedback(self, data: Dict) -> str:
        """Generate basic feedback based on extracted data"""
        feedback_points = []
        
        if len(data['skills']) < 5:
            feedback_points.append("Consider adding more technical skills to your CV")
        else:
            feedback_points.append("Good range of technical skills listed")

        if data['experience'] < 2:
            feedback_points.append("For junior roles, highlight relevant projects and educational achievements")
        else:
            feedback_points.append(f"Strong experience of {data['experience']} years in the field")

        if data['education']:
            feedback_points.append("Education section is well structured")
        else:
            feedback_points.append("Consider adding more detail to your educational background")

        return " ".join(feedback_points)

    def extract_data(self, cv_text: str) -> Dict:
        """Extract all CV data using regex patterns"""
        lines = cv_text.split('\n')
       # Get name from first line
        name = lines[0].strip() if lines else ""
    
        # Extract and clean email
        email_match = re.search(r'[\w.+-]+@[\w-]+\.[\w.-]+', cv_text)
        email = email_match.group(0).lower().strip() if email_match else None
        
        # Clean phone number
        phone_match = re.search(r'08[5-9][-\s]?\d{3}[-\s]?\d{4}', cv_text)
        phone = phone_match.group(0).replace(' ', '-') if phone_match else None
        
        # Extract skills
        skills_section = ""
        in_skills = False
        for line in lines:
            if 'COMPUTER SKILLS:' in line.upper():
                in_skills = True
                continue
            if in_skills and line.strip():
                skills_section = line.strip()
                break
        
        skills = [s.strip() for s in skills_section.replace(',', ' ').split()]
        
        # Extract education (everything between EDUCATION: and COMPUTER SKILLS:)
        education = []
        in_education = False
        for line in lines:
            if 'EDUCATION:' in line.upper():
                in_education = True
                continue
            if 'COMPUTER SKILLS:' in line.upper():
                break
            if in_education and line.strip():
                education.append(line.strip())
        
        # Calculate experience from years mentioned
        years = set()
        for line in cv_text.split('\n'):
            year_matches = re.finditer(r'20\d{2}', line)
            years.update(int(match.group()) for match in year_matches)
        
        experience = max(years) - min(years) if years else 0
        
        # Extract Dublin address
        address_match = re.search(r'([^,\n]+,\s*[^,\n]+,\s*Dublin\s*\d{1,2})', cv_text)
        location = address_match.group(1) if address_match else ""

        return {
            "name": name,
            "email": email,
            "phone": phone,
            "skills": skills,
            "experience": experience,
            "domain": "Technology",
            "education": education,
            "location": location,
            "feedback": ""
        }

    def basic_extraction(self, cv_text: str) -> Dict:
        """Minimal fallback extraction"""
        lines = cv_text.split('\n')
        return {
            "name": lines[0].strip() if lines else "",
            "email": None,
            "phone": None,
            "skills": [],
            "experience": 0,
            "domain": "Technology",
            "education": [],
            "location": "",
            "feedback": "Basic extraction used"
        }