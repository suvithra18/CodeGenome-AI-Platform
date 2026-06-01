from django.db import models

class Student(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    github_username = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class CodingScore(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    problem_name = models.CharField(max_length=100)
    score = models.IntegerField()
    attempts = models.IntegerField()
    time_taken = models.IntegerField()

    def __str__(self):
        return self.problem_name


class SkillReport(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    logic_score = models.FloatField()
    debugging_score = models.FloatField()
    consistency_score = models.FloatField()
    overall_score = models.FloatField()
    speed_score = models.FloatField()
    developer_level = models.CharField(max_length=50)
    improvement_tips = models.TextField()

    recommended_role = models.CharField(max_length=100)

    job_readiness = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.student.name
    
class InterviewScore(models.Model):

    student = models.ForeignKey(Student,
                                on_delete=models.CASCADE)

    mock_interview_score = models.FloatField()

    resume_score = models.FloatField()

    aptitude_score = models.FloatField()

    communication_score = models.FloatField()

    overall_interview_score = models.FloatField()

    interview_status = models.CharField(max_length=50)

    created_at = models.DateTimeField(auto_now_add=True)
    improvement_tips = models.TextField()

    recommended_company_type = models.CharField(max_length=100)

    def __str__(self):

        return f"{self.student.name} Interview Report"

class Resume(models.Model):

    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE
    )

    resume_file = models.FileField(
        upload_to='resumes/'
    )

    extracted_text = models.TextField(
        blank=True,
        null=True
    )

    resume_score = models.FloatField(
        default=0
    )

    ai_suggestions = models.TextField(
        blank=True,
        null=True
    )

    uploaded_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):

        return self.student.name

class MockInterview(models.Model):

    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE
    )

    question = models.TextField( blank=True,
    null=True)

    answer = models.TextField()

    score = models.FloatField(default=0)

    feedback = models.TextField()

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):

        return self.student.name

class WeeklyGrowth(models.Model):

    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE
    )

    week = models.CharField(max_length=50)

    coding_score = models.FloatField()

    interview_score = models.FloatField()

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):

        return self.student.name
    

    
class CodingChallenge(models.Model):

    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE
    )

    question = models.TextField()

    answer = models.TextField()

    score = models.IntegerField()

    feedback = models.TextField()

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):

        return self.student.name

STATUS_CHOICES = [

    ('Applied', 'Applied'),

    ('Interview Scheduled', 'Interview Scheduled'),

    ('Technical Round', 'Technical Round'),

    ('HR Round', 'HR Round'),

    ('Selected', 'Selected'),

    ('Rejected', 'Rejected')

]


class PlacementTracker(models.Model):

    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE
    )

    company_name = models.CharField(
        max_length=100
    )

    role = models.CharField(
        max_length=100
    )

    package = models.CharField(
        max_length=50
    )

    interview_round = models.CharField(
        max_length=100
    )

    hr_feedback = models.TextField()

    status = models.CharField(
        max_length=50,
        choices=STATUS_CHOICES,
        default='Applied'
    )

    applied_date = models.DateField()

    def __str__(self):

        return self.company_name