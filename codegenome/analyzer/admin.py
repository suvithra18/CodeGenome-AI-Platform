from django.contrib import admin
from .models import Student, CodingScore, SkillReport,InterviewScore,Resume,MockInterview,PlacementTracker

admin.site.register(Student)
admin.site.register(CodingScore)
admin.site.register(SkillReport)
admin.site.register(InterviewScore)

admin.site.register(Resume)



admin.site.register(MockInterview)

admin.site.register(PlacementTracker)

