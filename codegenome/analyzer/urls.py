from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('add-report/',views.add_skill_report,name='add_report'),
    path('view-reports/',views.view_reports,name='view_reports'),
    path('add-interview-score/',views.add_interview_score,name='add_interview_score'),
    path('view-interview-scores/',views.view_interview_scores,name='view_interview_scores'),
    path('combined-reports/',views.combined_reports,name='combined_reports'),
    path(  'leaderboard/',  views.leaderboard,name='leaderboard'),
    
    path('download-report/<int:student_id>/',views.download_pdf_report,name='download_pdf_report'),
    path('github-profile/<int:student_id>/',views.github_profile,name='github_profile'),
    path('resume-analyzer/',views.resume_analyzer,name='resume_analyzer'),
    path('career-suggestions/<int:student_id>/',views.career_suggestions,name='career_suggestions'),
    path('mock-interview/',views.mock_interview,name='mock_interview'),
    path('skill-gap/<int:student_id>/',views.skill_gap_analyzer,name='skill_gap'),
    
    path('certificate/<int:student_id>/',views.generate_certificate,name='generate_certificate'),
    path('coding-challenge/',views.coding_challenge,name='coding_challenge'),
    path('admin-analytics/',views.admin_analytics,name='admin_analytics'),
    path( 'chatbot/',views.chatbot,name='chatbot'),
    path('portfolio/<int:student_id>/',views.portfolio,name='portfolio'),
    path( 'placement-tracker/<int:student_id>/', views.placement_tracker, name='placement_tracker'),
]