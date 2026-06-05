# 🤖 AI Resume Analyzer

[![Deployed on Render](https://img.shields.io/badge/Deployed%20on-Render-46E3B7)](https://ai-career-copilot-gn3t.onrender.com)
[![Python](https://img.shields.io/badge/Python-3.11-blue)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-3.0-red)](https://flask.palletsprojects.com/)
[![Groq](https://img.shields.io/badge/Groq-API-orange)](https://groq.com/)

## 📌 Live Demo

**Try it here:** [https://ai-career-copilot-gn3t.onrender.com](https://ai-career-copilot-gn3t.onrender.com)

## 📖 About

AI Resume Analyzer is a web application that uses artificial intelligence to analyze resumes and provide personalized career guidance. Built with Flask and powered by Groq's LLM API, it helps job seekers understand their strengths, identify skill gaps, and prepare for interviews.

## ✨ Features

- 📄 **Resume Parsing** - Paste text or upload PDF/DOCX files
- 🎯 **Role-Based Analysis** - Analyze against any job role
- 📊 **Skill Detection** - Identifies your current skills
- ⚠️ **Gap Analysis** - Shows missing skills for target role
- 🗺️ **Career Roadmap** - Personalized learning path
- 💡 **Interview Questions** - Role-specific questions
- 📚 **History Tracking** - Save and review past analyses
- 🔐 **User Authentication** - Secure signup/login system

## 🛠️ Tech Stack

| Category | Technology |
|----------|------------|
| **Backend** | Flask 3.0 (Python) |
| **Database** | SQLite / PostgreSQL |
| **AI/ML** | Groq LLM API (Llama 3.3) |
| **Authentication** | Session-based |
| **Frontend** | HTML5, CSS3, Jinja2 |
| **Deployment** | Render (Gunicorn) |
| **File Parsing** | PyPDF2, python-docx |

## 📁 Project Structure

AI-Resume-Analyzer/
├── app.py # Main Flask application
├── ai.py # Groq API integration
├── db.py # Database configuration
├── models.py # SQLAlchemy models
├── config.py # Configuration settings
├── requirements.txt # Python dependencies
├── wsgi.py # Production entry point
├── .env # Environment variables (not in repo)
├── .gitignore # Git ignore rules
├── templates/ # HTML templates
│ ├── base.html
│ ├── dashboard.html
│ ├── history.html
│ ├── login.html
│ └── signup.html
└── static/ # CSS and assets


## 🚀 Installation (Local Development)

### Prerequisites
- Python 3.11+
- Git

### Step 1: Clone the repository
bash
git clone https://github.com/Bhushan-3IT/AI-Resume-Analyzer.git
cd AI-Resume-Analyzer

###step 2
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

###step 3
pip install -r requirements.txt

###step 4
GROQ_API_KEY=your_groq_api_key_here
SECRET_KEY=your_secret_key_here
DATABASE_URL=sqlite:///users.db
FLASK_ENV=development

python app.py
