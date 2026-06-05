from flask import Flask, redirect, render_template, request, session, url_for
from dotenv import load_dotenv
import os
import json
import secrets
from datetime import timedelta
import PyPDF2
import docx


load_dotenv()

from config import config


app = Flask(__name__, 
            static_folder='static',
            template_folder='templates')

env = os.environ.get('FLASK_ENV', 'development')
app.config.from_object(config[env])


app.secret_key = os.environ.get('SECRET_KEY', secrets.token_hex(32))
app.config['SESSION_PERMANENT'] = True
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=24)

from db import Base, engine, SessionLocal
import models
from ai import analyze_resume

# Create tables
Base.metadata.create_all(bind=engine)
# Get database session
db = SessionLocal()

@app.route("/") 
def home():
    if "user" in session:
        return redirect("/dashboard")
    return redirect("/login")

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        # Use models.User instead of User
        user = db.query(models.User).filter_by(email=email, password=password).first()
        if user:
            session.clear()
            session['user'] = email
            session['user_id'] = user.id
            session['logged_in'] = True
            return redirect(url_for('dashboard'))
        else:
            return "Invalid credentials! Please try again."
    
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        # Validate password length
        if len(password) < 6:
            return "Password must be at least 6 characters!"
        
        # Check if user exists
        existing_user = db.query(models.User).filter_by(email=email).first()
        if existing_user:
            return "User already exists! Please login."
        
        # Create new user
        new_user = models.User(email=email, password=password)
        db.add(new_user)
        db.commit()
        
        session.clear()
        session['user'] = email
        session['user_id'] = new_user.id
        session['logged_in'] = True
        return redirect(url_for('dashboard'))
    
    return render_template('signup.html')

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if 'user' not in session:
        return redirect(url_for('login'))
    
    # Check if user_id exists in session
    if 'user_id' not in session:
        user = db.query(models.User).filter_by(email=session['user']).first()
        if user:
            session['user_id'] = user.id
        else:
            return redirect(url_for('login'))
    
    result = None
    
    if request.method == 'POST':
        role = request.form.get('role')
        resume_text = request.form.get('resume', '')
        
        # Handle file upload
        if 'file' in request.files:
            file = request.files['file']
            if file and file.filename != '':
                try:
                    # Handle different file types
                    if file.filename.endswith('.pdf'):
                        # Handle PDF
                        pdf_reader = PyPDF2.PdfReader(file)
                        resume_text = ""
                        for page in pdf_reader.pages:
                            resume_text += page.extract_text()
                    elif file.filename.endswith('.docx'):
                        # Handle DOCX
                        doc = docx.Document(file)
                        resume_text = "\n".join([paragraph.text for paragraph in doc.paragraphs])
                    else:
                        # Handle text files
                        resume_text = file.read().decode('utf-8')
                except Exception as e:
                    result = {"error": f"Could not read file: {str(e)}"}
        
        if resume_text and role and not result:
            # Get AI analysis
            ai_result = analyze_resume(resume_text, role)
            
            if "error" in ai_result:
                result = ai_result
            else:
                # Format for template
                result = {
                    "skills": ai_result.get('strengths', []),
                    "missing-skills": ai_result.get('weaknesses', []),
                    "roadmap": ai_result.get('suggestions', []),
                    "interview_quetions": ai_result.get('interview_quetions', [
                        "Tell me about yourself",
                        "Why do you want this role?",
                        "Describe a challenging project"
                    ]),
                    "score": ai_result.get('score', 0),
                    "career_advice": ai_result.get('career_advice', '')
                }
                
                # Save to database - Use models.Reports
                report = models.Reports(
                    user_id=session['user_id'],
                    resume_text=resume_text[:500],
                    result=json.dumps({
                        "role": role,
                        "skills": ai_result.get('strengths', []),
                        "missing_skills": ai_result.get('weaknesses', []),
                        "roadmap": ai_result.get('suggestions', []),
                        "interview_questions": ai_result.get('interview_quetions', []),
                        "score": ai_result.get('score', 0),
                        "career_advice": ai_result.get('career_advice', '')
                    })
                )
                db.add(report)
                db.commit()
                
        elif not resume_text:
            result = {"error": "Please provide resume text or upload a file"}
        elif not role:
            result = {"error": "Please enter a role"}
    
    return render_template('dashboard.html', user=session['user'], result=result)

@app.route('/history')
def history():
    if 'user' not in session:
        return redirect(url_for('login'))
    
    # Get all reports for this user
    reports_data = db.query(models.Reports).filter_by(user_id=session['user_id']).order_by(models.Reports.id.desc()).all()
    
    # Parse the JSON results
    history_reports = []
    for report in reports_data:
        try:
            result_data = json.loads(report.result)
            history_reports.append({
                'resume': report.resume_text,
                'role': result_data.get('role', 'N/A'),
                'skills': result_data.get('skills', []),
                'missing-skills': result_data.get('missing_skills', []),
                'roadmap': result_data.get('roadmap', []),
                'interview_quetions': result_data.get('interview_questions', []),
                'score': result_data.get('score', 0),
                'analyzed_at': result_data.get('analyzed_at', '')
            })
        except:
            history_reports.append({
                'resume': report.resume_text,
                'role': 'Unknown',
                'skills': [],
                'missing-skills': [],
                'roadmap': [],
                'interview_quetions': [],
                'score': 0,
                'analyzed_at': ''
            })
    
    return render_template('history.html', user=session['user'], reports=history_reports)

@app.route("/logout")
def logout():
    session.pop("user", None)
    session.pop("user_id", None)
    return redirect("/login")

if __name__ == "__main__":
    app.run(debug=True)