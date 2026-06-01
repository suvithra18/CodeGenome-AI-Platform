from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.db.models import Avg
from reportlab.pdfgen import canvas
from .models import Student, SkillReport, InterviewScore,MockInterview,WeeklyGrowth, PlacementTracker,CodingChallenge

from .forms import CodingChallengeForm, StudentForm, SkillReportForm, InterviewScoreForm,MockInterviewForm

from django.contrib.auth.decorators import login_required
import requests,random


def index(request):

    return render(request,
                  'analyzer/index.html')


def register(request):

    if request.method == 'POST':

        form = StudentForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('dashboard')

    else:

        form = StudentForm()

    return render(request,
                  'analyzer/register.html',
                  {'form': form})


@login_required
def dashboard(request):

    students = Student.objects.all()

    reports = SkillReport.objects.all()

    # TOP PERFORMERS

    top_performers = SkillReport.objects.order_by(
        '-overall_score'
    )[:5]

    # AVERAGE SCORE

    average_score = reports.aggregate(
        Avg('overall_score')
    )['overall_score__avg']

    if average_score is None:

        average_score = 0

    # RECENT ACTIVITIES

    recent_reports = SkillReport.objects.order_by(
        '-created_at'
    )[:5]

    recent_interviews = InterviewScore.objects.order_by(
        '-created_at'
    )[:5]

    context = {

        'students': students,

        'reports': reports,

        'average_score': round(average_score, 2),

        'recent_reports': recent_reports,

        'recent_interviews': recent_interviews,

        'top_performers': top_performers

    }

    return render(request,
                  'analyzer/dashboard.html',
                  context)

def view_reports(request):

    reports = SkillReport.objects.all()

    return render(request,
                  'analyzer/view_reports.html',
                  {'reports': reports})




def add_skill_report(request):

    if request.method == 'POST':

        form = SkillReportForm(request.POST)

        if form.is_valid():

            report = form.save(commit=False)

            # CALCULATE OVERALL SCORE

            report.overall_score = (

                report.logic_score +
                report.debugging_score +
                report.consistency_score +
                report.speed_score

            ) / 4

            # ASSIGN LEVEL

            if report.overall_score >= 80:

                report.developer_level = "Advanced"

            elif report.overall_score >= 50:

                report.developer_level = "Intermediate"

            else:

                report.developer_level = "Beginner"

            report.save()

            return redirect('view_reports')

    else:

        form = SkillReportForm()

    return render(request,
                  'analyzer/add_skill_report.html',
                  {'form': form})



def add_interview_score(request):

    if request.method == 'POST':

        form = InterviewScoreForm(request.POST)

        if form.is_valid():

            interview = form.save(commit=False)

            # CALCULATE OVERALL SCORE

            interview.overall_interview_score = (

                interview.mock_interview_score +
                interview.resume_score +
                interview.aptitude_score +
                interview.communication_score

            ) / 4

            # STATUS

            if interview.overall_interview_score >= 80:

                interview.interview_status = "Placement Ready"

            elif interview.overall_interview_score >= 50:

                interview.interview_status = "Needs Improvement"

            else:

                interview.interview_status = "Beginner"

            interview.save()

            return redirect('view_interview_scores')

    else:

        form = InterviewScoreForm()

    return render(request,
                  'analyzer/add_interview_score.html',
                  {'form': form})


def view_interview_scores(request):

    interviews = InterviewScore.objects.all()

    return render(request,
                  'analyzer/view_interview_scores.html',
                  {'interviews': interviews})

from .models import SkillReport, InterviewScore


def combined_reports(request):

    reports = SkillReport.objects.all()

    combined_data = []

    for report in reports:

        # Get interview record
        interview = InterviewScore.objects.filter(
            student=report.student
        ).first()

        suggestions = []

        # =========================
        # SKILL ANALYSIS
        # =========================

        # LOGIC SCORE
        if report.logic_score < 30:
            suggestions.append(
                "Critical improvement needed in problem-solving."
            )

        elif report.logic_score < 50:
            suggestions.append(
                "Practice medium-level DSA problems regularly."
            )

        elif report.logic_score >= 80:
            suggestions.append(
                "Excellent logical thinking skills."
            )

        # DEBUGGING SCORE
        if report.debugging_score < 30:
            suggestions.append(
                "Spend more time fixing real-time project bugs."
            )

        elif report.debugging_score < 50:
            suggestions.append(
                "Improve debugging using VS Code debugging tools."
            )

        elif report.debugging_score >= 80:
            suggestions.append(
                "Strong debugging capability detected."
            )

        # CONSISTENCY SCORE
        if report.consistency_score < 30:
            suggestions.append(
                "Coding consistency is very low."
            )

        elif report.consistency_score < 50:
            suggestions.append(
                "Maintain a daily coding practice schedule."
            )

        elif report.consistency_score >= 80:
            suggestions.append(
                "Excellent learning consistency."
            )

        # SPEED SCORE
        if report.speed_score < 30:
            suggestions.append(
                "Improve coding speed through contests."
            )

        elif report.speed_score < 50:
            suggestions.append(
                "Practice timed coding exercises."
            )

        elif report.speed_score >= 80:
            suggestions.append(
                "Very good coding speed."
            )

        # =========================
        # INTERVIEW ANALYSIS
        # =========================

        if interview:

            # COMMUNICATION
            if interview.communication_score < 40:
                suggestions.append(
                    "Communication confidence needs improvement."
                )

            elif interview.communication_score >= 80:
                suggestions.append(
                    "Excellent communication skills."
                )

            # RESUME
            if interview.resume_score < 40:
                suggestions.append(
                    "Add strong projects and certifications to resume."
                )

            elif interview.resume_score >= 80:
                suggestions.append(
                    "Resume quality is impressive."
                )

            # APTITUDE
            if interview.aptitude_score < 40:
                suggestions.append(
                    "Practice aptitude questions daily."
                )

            elif interview.aptitude_score >= 80:
                suggestions.append(
                    "Strong aptitude performance."
                )

        # Remove duplicate suggestions
        suggestions = list(set(suggestions))

        # Default message
        if not suggestions:
            suggestions.append(
                "Overall performance is balanced. Keep improving consistently."
            )

        # =========================
        # CAREER STATUS
        # =========================

        if report.overall_score >= 80:

            career = (
                "Placement Ready for Product Companies"
            )

        elif report.overall_score >= 50:

            career = (
                "Almost Placement Ready"
            )

        else:

            career = (
                "Needs Improvement Before Placements"
            )

        # Append data
        combined_data.append({

            'skill': report,
            'interview': interview,
            'suggestions': suggestions,
            'career': career

        })

    return render(
        request,
        'analyzer/combined_reports.html',
        {'combined_data': combined_data}
    )

@login_required
def leaderboard(request):

    leaderboard_data = SkillReport.objects.order_by(
        '-overall_score'
    )

    return render(request,
                  'analyzer/leaderboard.html',
                  {
                      'leaderboard_data': leaderboard_data
                  })



def download_pdf_report(request, student_id):

    student = Student.objects.get(id=student_id)

    skill = SkillReport.objects.filter(
        student=student
    ).first()

    interview = InterviewScore.objects.filter(
        student=student
    ).first()

    response = HttpResponse(
        content_type='application/pdf'
    )

    response['Content-Disposition'] = (
        f'attachment; filename="{student.name}_report.pdf"'
    )

    p = canvas.Canvas(response)

    # TITLE

    p.setFont("Helvetica-Bold", 18)

    p.drawString(
        180,
        800,
        "CodeGenome AI Report"
    )

    # STUDENT DETAILS

    p.setFont("Helvetica", 12)

    p.drawString(
        50,
        760,
        f"Student Name: {student.name}"
    )

    p.drawString(
        50,
        740,
        f"Email: {student.email}"
    )

    p.drawString(
        50,
        720,
        f"GitHub: {student.github_username}"
    )

    # SKILL REPORT

    y = 680

    p.setFont("Helvetica-Bold", 14)

    p.drawString(
        50,
        y,
        "Skill Analytics"
    )

    p.setFont("Helvetica", 12)

    y -= 30

    if skill:

        p.drawString(
            50,
            y,
            f"Logic Score: {skill.logic_score}"
        )

        y -= 20

        p.drawString(
            50,
            y,
            f"Debugging Score: {skill.debugging_score}"
        )

        y -= 20

        p.drawString(
            50,
            y,
            f"Consistency Score: {skill.consistency_score}"
        )

        y -= 20

        p.drawString(
            50,
            y,
            f"Speed Score: {skill.speed_score}"
        )

        y -= 20

        p.drawString(
            50,
            y,
            f"Overall Score: {skill.overall_score}"
        )

        y -= 20

        p.drawString(
            50,
            y,
            f"Developer Level: {skill.developer_level}"
        )

    # INTERVIEW REPORT

    y -= 50

    p.setFont("Helvetica-Bold", 14)

    p.drawString(
        50,
        y,
        "Interview Analytics"
    )

    p.setFont("Helvetica", 12)

    y -= 30

    if interview:

        p.drawString(
            50,
            y,
            f"Mock Interview: {interview.mock_interview_score}"
        )

        y -= 20

        p.drawString(
            50,
            y,
            f"Resume Score: {interview.resume_score}"
        )

        y -= 20

        p.drawString(
            50,
            y,
            f"Aptitude Score: {interview.aptitude_score}"
        )

        y -= 20

        p.drawString(
            50,
            y,
            f"Communication Score: {interview.communication_score}"
        )

        y -= 20

        p.drawString(
            50,
            y,
            f"Overall Interview Score: {interview.overall_interview_score}"
        )

    # AI SUGGESTIONS

    y -= 50

    p.setFont("Helvetica-Bold", 14)

    p.drawString(
        50,
        y,
        "AI Suggestions"
    )

    p.setFont("Helvetica", 12)

    y -= 30

    suggestions = []

    if skill:

        if skill.logic_score < 50:

            suggestions.append(
                "Improve problem-solving skills."
            )

        if skill.debugging_score < 50:

            suggestions.append(
                "Practice debugging projects."
            )

        if skill.speed_score < 50:

            suggestions.append(
                "Participate in coding contests."
            )

    if interview:

        if interview.communication_score < 50:

            suggestions.append(
                "Improve communication skills."
            )

    if len(suggestions) == 0:

        suggestions.append(
            "Excellent performance. Keep improving advanced skills."
        )

    for tip in suggestions:

        p.drawString(
            60,
            y,
            f"- {tip}"
        )

        y -= 20

    # FOOTER

    y -= 40

    p.setFont("Helvetica-Bold", 12)

    p.drawString(
        50,
        y,
        "Generated by CodeGenome AI Platform"
    )

    p.showPage()

    p.save()

    return response

def github_profile(request, student_id):

    student = Student.objects.get(id=student_id)

    github_data = None

    repositories = []

    if student.github_username:

        # USER PROFILE API

        profile_url = (
            f"https://api.github.com/users/"
            f"{student.github_username}"
        )

        response = requests.get(profile_url)

        if response.status_code == 200:

            github_data = response.json()

        # REPOSITORIES API

        repo_url = (
            f"https://api.github.com/users/"
            f"{student.github_username}/repos"
        )

        repo_response = requests.get(repo_url)

        if repo_response.status_code == 200:

            repositories = repo_response.json()

    context = {

        'student': student,

        'github_data': github_data,

        'repositories': repositories

    }

    return render(request,
                  'analyzer/github_profile.html',
                  context)

from PyPDF2 import PdfReader

from .forms import ResumeForm

from .models import Resume


def resume_analyzer(request):

    score = None

    suggestions = []

    extracted_text = ""

    if request.method == 'POST':

        form = ResumeForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():

            resume = form.save()

            pdf_file = request.FILES['resume_file']

            pdf_reader = PdfReader(pdf_file)

            text = ""    

            for page in pdf_reader.pages:

                text += page.extract_text()

            resume.extracted_text = text

            extracted_text = text

            # SKILL DETECTION

            skills = [

                'python',
                'django',
                'mysql',
                'html',
                'css',
                'javascript',
                'react',
                'git',
                'api'
            ]

            found_skills = []

            for skill in skills:

                if skill.lower() in text.lower():

                    found_skills.append(skill)

            # SCORE CALCULATION

            score = len(found_skills) * 10

            if score > 100:

                score = 100

            resume.resume_score = score

            # AI SUGGESTIONS

            missing_skills = list(
                set(skills) - set(found_skills)
            )

            if len(missing_skills) > 0:

                suggestions.append(
                    "Add these skills to improve resume:"
                )

                suggestions.extend(missing_skills)

            else:

                suggestions.append(
                    "Excellent technical resume."
                )

            resume.ai_suggestions = (
                ", ".join(suggestions)
            )

            resume.save()

            return render(
                request,
                'analyzer/resume_result.html',
                {

                    'resume': resume,

                    'score': score,

                    'found_skills': found_skills,

                    'suggestions': suggestions,

                    'text': extracted_text

                }
            )

    else:

        form = ResumeForm()

    return render(request,
                  'analyzer/resume_analyzer.html',
                  {'form': form})

def career_suggestions(request, student_id):

    student = Student.objects.get(id=student_id)

    skill = SkillReport.objects.filter(
        student=student
    ).first()

    interview = InterviewScore.objects.filter(
        student=student
    ).first()

    resume = Resume.objects.filter(
        student=student
    ).first()

    # DEFAULT VALUES

    career_role = ""

    company_type = ""

    technologies = []

    suggestions = []

    readiness = ""

    # SCORES

    logic = skill.logic_score if skill else 0

    debugging = skill.debugging_score if skill else 0

    speed = skill.speed_score if skill else 0

    consistency = skill.consistency_score if skill else 0

    communication = (
        interview.communication_score
        if interview else 0
    )

    resume_score = (
        resume.resume_score
        if resume else 0
    )

    # AVERAGE SCORE

    overall = (
        logic +
        debugging +
        speed +
        consistency +
        communication +
        resume_score
    ) / 6

    # DYNAMIC CAREER ENGINE

    # FULL STACK

    if logic >= 80 and debugging >= 75:

        career_role = "Full Stack Developer"

        company_type = "Product-Based Companies"

        technologies = [

            "Django",
            "React",
            "REST API",
            "Docker",
            "AWS"

        ]

    # BACKEND

    elif debugging >= 80 and consistency >= 70:

        career_role = "Backend Developer"

        company_type = "Service-Based Companies"

        technologies = [

            "Python",
            "Django",
            "MySQL",
            "API Development"

        ]

    # FRONTEND

    elif communication >= 75 and speed >= 70:

        career_role = "Frontend Developer"

        company_type = "UI/UX & Web Companies"

        technologies = [

            "HTML",
            "CSS",
            "JavaScript",
            "React"

        ]

    # DATA ANALYST

    elif logic >= 70 and consistency >= 70:

        career_role = "Data Analyst"

        company_type = "Analytics Companies"

        technologies = [

            "Python",
            "Pandas",
            "SQL",
            "Power BI"

        ]

    # TRAINEE

    else:

        career_role = "Software Engineer Trainee"

        company_type = "Startup / Internship Companies"

        technologies = [

            "Python Basics",
            "HTML",
            "CSS",
            "SQL"

        ]

    # READINESS

    if overall >= 85:

        readiness = "Placement Ready"

    elif overall >= 60:

        readiness = "Almost Ready"

    else:

        readiness = "Needs Improvement"

    # AI SUGGESTIONS

    if logic < 50:

        suggestions.append(
            "Improve problem-solving skills."
        )

    if debugging < 50:

        suggestions.append(
            "Practice debugging projects."
        )

    if speed < 50:

        suggestions.append(
            "Improve coding speed."
        )

    if communication < 50:

        suggestions.append(
            "Practice mock interviews."
        )

    if resume_score < 50:

        suggestions.append(
            "Improve resume quality."
        )

    if len(suggestions) == 0:

        suggestions.append(
            "Excellent profile for placements."
        )

    context = {
        'career_role': career_role,
        'company_type': company_type,
        'technologies': technologies,
        'suggestions': suggestions,
        'readiness': readiness,
        'overall': overall,
        'logic': logic,
        'debugging': debugging,
        'speed': speed,
        'consistency': consistency,
        'communication': communication,
        'resume_score': resume_score,
        'student': student,
    }

    return render(
        request,
        'analyzer/career_suggestions.html',
        context
    )
def mock_interview(request):

    questions = [

        "Explain your recent Python project.",

        "What is Django ORM?",

        "Difference between list and tuple?",

        "How does API integration work?",

        "Explain REST API.",

        "What is debugging?",

        "Tell me about a challenging project.",

        "What is database normalization?",

        "How do you handle errors in Python?",

        "Explain OOP concepts in Python."

    ]

    random_question = random.choice(
        questions
    )

    if request.method == 'POST':

        form = MockInterviewForm(request.POST)

        question = request.POST.get(
            'question'
        )

        if form.is_valid():

            interview = form.save(
                commit=False
            )

            # IMPORTANT
            interview.question = question

            answer = interview.answer.lower()

            score = 0

            matched = 0

            # QUESTION BASED KEYWORDS

            question_keywords = {

                "Explain your recent Python project.": [
                    'python',
                    'project',
                    'django',
                    'api'
                ],

                "What is Django ORM?": [
                    'django',
                    'orm',
                    'database',
                    'queryset',
                    'model'
                ],

                "Difference between list and tuple?": [
                    'list',
                    'tuple',
                    'mutable',
                    'immutable'
                ],

                "How does API integration work?": [
                    'api',
                    'request',
                    'response',
                    'json'
                ],

                "Explain REST API.": [
                    'rest',
                    'api',
                    'http',
                    'json'
                ],

                "What is debugging?": [
                    'debugging',
                    'error',
                    'bug',
                    'fix'
                ],

                "Tell me about a challenging project.": [
                    'project',
                    'challenge',
                    'solution',
                    'team'
                ],

                "What is database normalization?": [
                    'database',
                    'normalization',
                    'table',
                    'redundancy'
                ],

                "How do you handle errors in Python?": [
                    'try',
                    'except',
                    'error',
                    'exception'
                ],

                "Explain OOP concepts in Python.": [
                    'class',
                    'object',
                    'inheritance',
                    'polymorphism'
                ]

            }

            keywords = question_keywords.get(
                question,
                []
            )

            for keyword in keywords:

                if keyword in answer:

                    matched += 1

            # SCORE

            score = matched * 20

            # BONUS

            if len(answer) > 100:

                score += 10

            if score > 100:

                score = 100

            interview.score = score

            # FEEDBACK

            if score >= 80:

                feedback = (
                    "Excellent technical explanation."
                )

            elif score >= 50:

                feedback = (
                    "Good answer with decent understanding."
                )

            else:

                feedback = (
                    "Need improvement in technical explanation."
                )

            # AI SUGGESTIONS

            suggestions = []

            missing_keywords = []

            for keyword in keywords:

                if keyword not in answer:

                    missing_keywords.append(
                        keyword
                    )

            if missing_keywords:

                suggestions.append(

                    "Try including keywords like: "

                    + ", ".join(missing_keywords)

                )

            else:

                suggestions.append(
                    "Excellent interview performance."
                )

            interview.feedback = (

                feedback +

                " Suggestions: " +

                ", ".join(suggestions)

            )

            interview.save()

            return render(

                request,

                'analyzer/mock_result.html',

                {

                    'interview': interview,

                    'feedback': feedback,

                    'suggestions': suggestions

                }

            )

    else:

        form = MockInterviewForm()

    return render(

        request,

        'analyzer/mock_interview.html',

        {

            'form': form,

            'question': random_question

        }

    )
def skill_gap_analyzer(request, student_id):

    student = Student.objects.get(id=student_id)

    skill = SkillReport.objects.filter(
        student=student
    ).first()

    resume = Resume.objects.filter(
        student=student
    ).first()

    # INDUSTRY REQUIRED SKILLS

    required_skills = [

        'python',
        'django',
        'mysql',
        'html',
        'css',
        'javascript',
        'react',
        'git',
        'api',
        'docker',
        'aws'

    ]

    # DETECTED SKILLS

    student_skills = []

    if resume:

        text = resume.extracted_text.lower()

        for tech in required_skills:

            if tech.lower() in text:

                student_skills.append(tech)

    # MISSING SKILLS

    missing_skills = list(
        set(required_skills) -
        set(student_skills)
    )

    # READINESS %

    readiness = (
        len(student_skills) /
        len(required_skills)
    ) * 100

    readiness = round(readiness, 2)

    # LEARNING ROADMAP

    roadmap = []

    if 'react' in missing_skills:

        roadmap.append(
            "Learn React for frontend development."
        )

    if 'docker' in missing_skills:

        roadmap.append(
            "Learn Docker for deployment."
        )

    if 'aws' in missing_skills:

        roadmap.append(
            "Learn AWS cloud fundamentals."
        )

    if 'api' in missing_skills:

        roadmap.append(
            "Practice REST API integration."
        )

    if 'git' in missing_skills:

        roadmap.append(
            "Use Git & GitHub regularly."
        )

    if len(roadmap) == 0:

        roadmap.append(
            "Excellent industry-ready profile."
        )

    context = {

        'student': student,

        'student_skills': student_skills,

        'missing_skills': missing_skills,

        'readiness': readiness,

        'roadmap': roadmap

    }

    return render(request,
                  'analyzer/skill_gap.html',
                  context)


def generate_certificate(request, student_id):

    student = Student.objects.get(
        id=student_id
    )

    response = HttpResponse(
        content_type='application/pdf'
    )

    response[
        'Content-Disposition'
    ] = (
        f'attachment; filename='
        f'"{student.name}_certificate.pdf"'
    )

    p = canvas.Canvas(response)

    # TITLE

    p.setFont(
        "Helvetica-Bold",
        28
    )

    p.drawCentredString(
        300,
        700,
        "Certificate of Achievement"
    )

    # STUDENT NAME

    p.setFont(
        "Helvetica",
        20
    )

    p.drawCentredString(
        300,
        620,
        f"This certificate is awarded to"
    )

    p.setFont(
        "Helvetica-Bold",
        24
    )

    p.drawCentredString(
        300,
        570,
        student.name
    )

    # MESSAGE

    p.setFont(
        "Helvetica",
        16
    )

    p.drawCentredString(
        300,
        500,
        "For outstanding performance in"
    )

    p.drawCentredString(
        300,
        470,
        "CodeGenome AI Skill Analytics"
    )

    # FOOTER

    p.drawString(
        50,
        100,
        "Generated by CodeGenome"
    )

    p.showPage()

    p.save()

    return response



def admin_analytics(request):

    total_students = Student.objects.count()

    avg_skill = SkillReport.objects.aggregate(
        Avg('overall_score')
    )

    avg_interview = InterviewScore.objects.aggregate(
        Avg('overall_interview_score')
    )

    return render(
        request,
        'analyzer/admin_analytics.html',
        {

            'total_students': total_students,

            'avg_skill': avg_skill,

            'avg_interview': avg_interview

        }
    )
def chatbot(request):

    response = ""

    if request.method == "POST":

        user_input = request.POST.get(
            'message'
        ).lower()

        # PYTHON

        if (
            "python" in user_input
            or "django" in user_input
        ):

            response = (
                "Practice Python fundamentals, Django ORM, "
                "REST APIs, and build real-time projects."
            )

        # INTERVIEW

        elif (
            "interview" in user_input
            or "hr" in user_input
        ):

            response = (
                "Focus on communication skills, "
                "project explanation, and mock interviews."
            )

        # RESUME

        elif "resume" in user_input:

            response = (
                "Keep your resume one page, add projects, "
                "GitHub links, and technical skills."
            )

        # DSA

        elif (
            "dsa" in user_input
            or "problem solving" in user_input
            or "leetcode" in user_input
        ):

            response = (
                "Practice arrays, strings, recursion, "
                "sorting, and daily LeetCode problems."
            )

        # FRONTEND

        elif (
            "frontend" in user_input
            or "react" in user_input
            or "javascript" in user_input
        ):

            response = (
                "Learn JavaScript ES6, React components, "
                "hooks, APIs, and responsive UI design."
            )

        # BACKEND

        elif (
            "backend" in user_input
            or "api" in user_input
        ):

            response = (
                "Focus on Django, REST API creation, "
                "authentication, and database optimization."
            )

        # DATABASE

        elif (
            "sql" in user_input
            or "database" in user_input
            or "mysql" in user_input
        ):

            response = (
                "Practice joins, normalization, indexing, "
                "queries, and database design concepts."
            )

        # GITHUB

        elif (
            "github" in user_input
            or "portfolio" in user_input
        ):

            response = (
                "Upload projects regularly, maintain README files, "
                "and build a strong portfolio."
            )

        # JOBS

        elif (
            "job" in user_input
            or "placement" in user_input
            or "career" in user_input
        ):

            response = (
                "Build strong projects, improve DSA, "
                "practice interviews, and maintain consistency."
            )

        # AI

        elif (
            "ai" in user_input
            or "machine learning" in user_input
        ):

            response = (
                "Learn Python, Pandas, NumPy, Scikit-learn, "
                "and work on AI mini projects."
            )

        # DEFAULT

        else:

            response = (
                "Please ask about Python, interviews, "
                "resume, DSA, frontend, backend, database, "
                "GitHub, AI, or placements."
            )

    return render(
        request,
        'analyzer/chatbot.html',
        {

            'response': response

        }
    )
def portfolio(request, student_id):

    student = Student.objects.get(
        id=student_id
    )

    # =========================
    # SKILL REPORT
    # =========================

    skill_report = SkillReport.objects.filter(
        student=student
    ).first()

    # =========================
    # RESUME
    # =========================

    resume = Resume.objects.filter(
        student=student
    ).first()

    # =========================
    # CODING CHALLENGES
    # =========================

    coding_challenges = CodingChallenge.objects.filter(
        student=student
    )

    # =========================
    # MOCK INTERVIEWS
    # =========================

    mock_interviews = MockInterview.objects.filter(
        student=student
    )

    # =========================
    # CODING AVERAGE
    # =========================

    coding_avg = 0

    if coding_challenges.exists():

        coding_avg = round(

            sum(
                challenge.score
                for challenge in coding_challenges
            ) / coding_challenges.count(),

            2

        )

    # =========================
    # MOCK INTERVIEW AVERAGE
    # =========================

    interview_avg = 0

    if mock_interviews.exists():

        interview_avg = round(

            sum(
                interview.score
                for interview in mock_interviews
            ) / mock_interviews.count(),

            2

        )

    # =========================
    # OVERALL SKILL SCORE
    # =========================

    overall_skill_score = 0

    if skill_report:

        overall_skill_score = (
            skill_report.overall_score
        )

    # =========================
    # RESUME SCORE
    # =========================

    resume_score = 0

    if resume:

        resume_score = (
            resume.resume_score
        )

    # =========================
    # PLACEMENT READINESS
    # =========================

    scores = []

    if coding_avg > 0:

        scores.append(coding_avg)

    if interview_avg > 0:

        scores.append(interview_avg)

    if resume_score > 0:

        scores.append(resume_score)

    if overall_skill_score > 0:

        scores.append(overall_skill_score)

    if len(scores) > 0:

        readiness = round(

            sum(scores) / len(scores),

            2

        )

    else:

        readiness = 0

    # =========================
    # CAREER ROLE
    # =========================

    career_role = "Software Engineer"

    if skill_report:

        if (
            skill_report.logic_score >= 80
            and
            skill_report.debugging_score >= 75
        ):

            career_role = (
                "Full Stack Developer"
            )

        elif (
            skill_report.debugging_score >= 80
        ):

            career_role = (
                "Backend Developer"
            )

        elif (
            skill_report.speed_score >= 75
        ):

            career_role = (
                "Frontend Developer"
            )

        elif (
            skill_report.logic_score >= 70
        ):

            career_role = (
                "Python Developer"
            )

    # =========================
    # SKILLS
    # =========================

    skills = []

    if skill_report:

        if skill_report.logic_score >= 70:

            skills.append(
                "Problem Solving"
            )

        if skill_report.debugging_score >= 70:

            skills.append(
                "Debugging"
            )

        if skill_report.speed_score >= 70:

            skills.append(
                "Fast Coding"
            )

        if skill_report.consistency_score >= 70:

            skills.append(
                "Consistency"
            )

    # =========================
    # ACHIEVEMENTS
    # =========================

    achievements = []

    # CODING

    if coding_challenges.exists():

        if coding_avg >= 80:

            achievements.append(
                "Top Coding Performer"
            )

        elif coding_avg >= 50:

            achievements.append(
                "Good Coding Skills"
            )

        else:

            achievements.append(
                "Coding Practice Needed"
            )

    else:

        achievements.append(
            "Coding Challenge Not Completed"
        )

    # MOCK INTERVIEW

    if mock_interviews.exists():

        if interview_avg >= 80:

            achievements.append(
                "Interview Expert"
            )

        elif interview_avg >= 50:

            achievements.append(
                "Good Communication Skills"
            )

        else:

            achievements.append(
                "Mock Interview Improvement Needed"
            )

    else:

        achievements.append(
            "Mock Interview Not Completed"
        )

    # RESUME

    if resume:

        if resume_score >= 80:

            achievements.append(
                "Professional Resume"
            )

        elif resume_score >= 50:

            achievements.append(
                "Resume Ready"
            )

        else:

            achievements.append(
                "Resume Needs Improvement"
            )

    else:

        achievements.append(
            "Resume Not Uploaded"
        )

    # READINESS

    if readiness >= 90:

        achievements.append(
            "Placement Ready"
        )

    elif readiness >= 75:

        achievements.append(
            "Almost Placement Ready"
        )

    elif readiness >= 50:

        achievements.append(
            "Placement Preparation Ongoing"
        )

    else:

        achievements.append(
            "Learning Stage"
        )

    # =========================
    # AI SUGGESTIONS
    # =========================

    suggestions = []

    # CODING ANALYSIS

    if coding_challenges.exists():

        if coding_avg >= 90:

            suggestions.append(
                "Outstanding coding performance with strong logic."
            )

        elif coding_avg >= 75:

            suggestions.append(
                "Good coding skills. Practice advanced DSA problems."
            )

        elif coding_avg >= 60:

            suggestions.append(
                "Average coding performance. Improve optimization techniques."
            )

        else:

            suggestions.append(
                "Focus on Python basics and daily coding practice."
            )

    else:

        suggestions.append(
            "Complete coding challenges to analyze coding skills."
        )

    # MOCK INTERVIEW ANALYSIS

    if mock_interviews.exists():

        if interview_avg >= 90:

            suggestions.append(
                "Excellent interview communication and confidence."
            )

        elif interview_avg >= 75:

            suggestions.append(
                "Good interview skills. Improve real-time examples."
            )

        elif interview_avg >= 60:

            suggestions.append(
                "Average interview performance. Practice technical explanations."
            )

        else:

            suggestions.append(
                "Improve communication and technical vocabulary."
            )

    else:

        suggestions.append(
            "Complete mock interviews to analyze communication skills."
        )

    # RESUME ANALYSIS

    if resume:

        if resume_score >= 90:

            suggestions.append(
                "Professional resume with strong industry readiness."
            )

        elif resume_score >= 75:

            suggestions.append(
                "Good resume. Add more projects and certifications."
            )

        elif resume_score >= 60:

            suggestions.append(
                "Improve resume formatting and project descriptions."
            )

        else:

            suggestions.append(
                "Add GitHub projects and internships to improve resume."
            )

    else:

        suggestions.append(
            "Upload resume for resume analysis."
        )

    # SKILL REPORT ANALYSIS

    if skill_report:

        # LOGIC

        if skill_report.logic_score >= 85:

            suggestions.append(
                "Strong logical thinking and analytical skills."
            )

        elif skill_report.logic_score >= 60:

            suggestions.append(
                "Good logical skills. Practice advanced problem solving."
            )

        else:

            suggestions.append(
                "Practice aptitude and logical coding exercises."
            )

        # DEBUGGING

        if skill_report.debugging_score >= 85:

            suggestions.append(
                "Excellent debugging capability."
            )

        elif skill_report.debugging_score >= 60:

            suggestions.append(
                "Good debugging skills with real-time applications."
            )

        else:

            suggestions.append(
                "Practice debugging real-world applications."
            )

        # SPEED

        if skill_report.speed_score >= 85:

            suggestions.append(
                "Very good coding speed and implementation skills."
            )

        elif skill_report.speed_score >= 60:

            suggestions.append(
                "Good coding speed. Practice timed challenges."
            )

        else:

            suggestions.append(
                "Improve coding speed using coding contests."
            )

        # CONSISTENCY

        if skill_report.consistency_score >= 85:

            suggestions.append(
                "Excellent learning consistency and dedication."
            )

        elif skill_report.consistency_score >= 60:

            suggestions.append(
                "Good consistency in coding practice."
            )

        else:

            suggestions.append(
                "Maintain a daily coding schedule."
            )

    else:

        suggestions.append(
            "Complete skill assessment for technical analysis."
        )

    # PLACEMENT READINESS

    if readiness >= 90:

        suggestions.append(
            "Highly placement ready for top product companies."
        )

    elif readiness >= 75:

        suggestions.append(
            "Good placement readiness. Focus on interview preparation."
        )

    elif readiness >= 60:

        suggestions.append(
            "Placement readiness is moderate. Improve weak areas."
        )

    else:

        suggestions.append(
            "Need improvement in coding and communication skills."
        )

    # REMOVE DUPLICATES

    suggestions = list(set(suggestions))

    # =========================
    # CONTEXT
    # =========================

    context = {

        'student': student,

        'skill_report': skill_report,

        'resume': resume,

        'coding_avg': coding_avg,

        'interview_avg': interview_avg,

        'overall_skill_score': overall_skill_score,

        'resume_score': resume_score,

        'readiness': readiness,

        'career_role': career_role,

        'skills': skills,

        'achievements': achievements,

        'suggestions': suggestions,

        'coding_challenges': coding_challenges,

        'mock_interviews': mock_interviews

    }

    return render(

        request,

        'analyzer/portfolio.html',

        context

    )
def placement_tracker(request, student_id):

    student = Student.objects.get(
        id=student_id
    )

    placements = PlacementTracker.objects.filter(
        student=student
    ).order_by('-applied_date')

    # COUNTS

    total_applications = placements.count()

    selected_count = placements.filter(
        status='Selected'
    ).count()

    rejected_count = placements.filter(
        status='Rejected'
    ).count()

    inprogress_count = placements.filter(
        status='In Progress'
    ).count()

    # SUCCESS RATE

    success_rate = 0

    if total_applications > 0:

        success_rate = round(

            (selected_count / total_applications) * 100,

            2

        )

    context = {

        'student': student,

        'placements': placements,

        'total_applications': total_applications,

        'selected_count': selected_count,

        'rejected_count': rejected_count,

        'inprogress_count': inprogress_count,

        'success_rate': success_rate
        

    }

    return render(
        request,
        'analyzer/placement_tracker.html',
        context
    )

import random


import random


def coding_challenge(request):

    questions = [

        "Write a Python program to reverse a string.",

        "Write a Python program to find palindrome.",

        "Write a Python program to sort a list.",

        "Write a Python program for Fibonacci series.",

        "Write a Python program to remove duplicates."

    ]

    random_question = random.choice(
        questions
    )

    if request.method == 'POST':

        form = CodingChallengeForm(
            request.POST
        )

        if form.is_valid():

            challenge = form.save(
                commit=False
            )

            challenge.question = request.POST.get(
                'question'
            )

            answer = challenge.answer.lower()

            # AI SCORING

            score = 0

            feedback_points = []

            # BASIC CODE LENGTH

            if len(answer) > 20:

                score += 20

            else:

                feedback_points.append(
                    "Code is too short."
                )

            # FUNCTION CHECK

            if "def " in answer:

                score += 20

            else:

                feedback_points.append(
                    "Use functions for better structure."
                )

            # LOOP CHECK

            if (
                "for " in answer
                or "while " in answer
            ):

                score += 15

            # RETURN CHECK

            if "return" in answer:

                score += 10

            # CONDITION CHECK

            if "if " in answer:

                score += 10

            # STRING/LIST OPERATIONS

            if (
                "[::-1]" in answer
                or ".append" in answer
                or "set(" in answer
                or "sort(" in answer
            ):

                score += 10

            # PRINT CHECK

            if "print" in answer:

                score += 10

            # CLEAN CODE BONUS

            if "\n" in challenge.answer:

                score += 5

            # LIMIT SCORE

            if score > 100:

                score = 100

            # FINAL FEEDBACK

            if score >= 90:

                final_feedback = (
                    "Excellent coding solution with strong logic."
                )

            elif score >= 75:

                final_feedback = (
                    "Good coding approach and structure."
                )

            elif score >= 50:

                final_feedback = (
                    "Average solution. Improve optimization."
                )

            else:

                final_feedback = (
                    "Need more coding practice."
                )

            # EXTRA FEEDBACK

            if feedback_points:

                final_feedback += " " + " ".join(
                    feedback_points
                )

            challenge.score = score

            challenge.feedback = final_feedback

            challenge.save()

           
            return render(

                request,

                'analyzer/challenge_result.html',

                {

                    'challenge': challenge

                }

            )

    else:

        form = CodingChallengeForm()

    return render(

        request,

        'analyzer/coding_challenge.html',

        {

            'form': form,

            'question': random_question

        }

    )