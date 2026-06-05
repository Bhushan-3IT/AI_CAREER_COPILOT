
from groq import Groq
import json
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get API key from environment variable
GROQ_API_KEY = os.environ.get('GROQ_API_KEY')

if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY not found in environment variables")

# Initialize Groq client
client = Groq(api_key=GROQ_API_KEY)

def analyze_resume(resume_text, user_goal):
    try:
        prompt = f"""
You are a senior software engineer and hiring manager.

Analyze the resume below based on the user's goal.

USER GOAL:
{user_goal}

RESUME:
{resume_text}

Return response in STRICT JSON format:
{{
    "score": 0-100,
    "strengths": [],
    "weaknesses": [],
    "suggestions": [],
    "career_advice": ""
}}
"""

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",  # Updated working model
            messages=[
                {"role": "system", "content": "You are an expert resume reviewer. Always return valid JSON."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=1000
        )

        result_text = response.choices[0].message.content
        
        # Clean the response
        result_text = result_text.strip()
        if result_text.startswith("```json"):
            result_text = result_text[7:]
        if result_text.startswith("```"):
            result_text = result_text[3:]
        if result_text.endswith("```"):
            result_text = result_text[:-3]
        result_text = result_text.strip()

        # Convert AI response to Python dict
        result = json.loads(result_text)
        
        # Add interview questions
        result["interview_quetions"] = [
            "Tell me about yourself",
            "Why are you interested in this role?",
            "Describe a challenging project you worked on",
            "How do you handle feedback and criticism?",
            "Where do you see yourself in 5 years?"
        ]

        return result

    except json.JSONDecodeError as e:
        return {
            "error": f"Failed to parse AI response: {str(e)}"
        }
    except Exception as e:
        return {
            "error": f"AI analysis failed: {str(e)}"
        }