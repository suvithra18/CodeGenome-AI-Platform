from django import forms

from .models import Student, SkillReport, InterviewScore, Resume, MockInterview,CodingChallenge


class StudentForm(forms.ModelForm):

    class Meta:

        model = Student

        fields = '__all__'

        widgets = {

            'name': forms.TextInput(attrs={
                'class': 'form-control'
            }),

            'email': forms.EmailInput(attrs={
                'class': 'form-control'
            }),

            'github_username': forms.TextInput(attrs={
                'class': 'form-control'
            }),
        }


class SkillReportForm(forms.ModelForm):

    class Meta:

        model = SkillReport

        fields = [
            'student',
            'logic_score',
            'debugging_score',
            'consistency_score',
            'speed_score'
        ]

        widgets = {

            'student': forms.Select(attrs={
                'class': 'form-control'
            }),

            'logic_score': forms.NumberInput(attrs={
                'class': 'form-control'
            }),

            'debugging_score': forms.NumberInput(attrs={
                'class': 'form-control'
            }),

            'consistency_score': forms.NumberInput(attrs={
                'class': 'form-control'
            }),

            'speed_score': forms.NumberInput(attrs={
                'class': 'form-control'
            }),
        }
    

class InterviewScoreForm(forms.ModelForm):

    class Meta:

        model = InterviewScore

        fields = [

            'student',
            'mock_interview_score',
            'resume_score',
            'aptitude_score',
            'communication_score'

        ]

        widgets = {

            'student': forms.Select(attrs={
                'class': 'form-control'
            }),

            'mock_interview_score': forms.NumberInput(attrs={
                'class': 'form-control'
            }),

            'resume_score': forms.NumberInput(attrs={
                'class': 'form-control'
            }),

            'aptitude_score': forms.NumberInput(attrs={
                'class': 'form-control'
            }),

            'communication_score': forms.NumberInput(attrs={
                'class': 'form-control'
            }),
        }

class ResumeForm(forms.ModelForm):

    class Meta:

        model = Resume

        fields = ['student', 'resume_file']

class MockInterviewForm(forms.ModelForm):

    class Meta:

        model = MockInterview

        fields = [

            'student',
           
            'answer'

        ]

        widgets = {

            'question': forms.Textarea(
                attrs={'rows': 3}
            ),

            'answer': forms.Textarea(
                attrs={'rows': 6}
            )

        }
class CodingChallengeForm(forms.ModelForm):

    class Meta:

        model = CodingChallenge

        fields = [

            'student',

            'answer'

        ]

        widgets = {

            'answer': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': 10
                }
            )

        }