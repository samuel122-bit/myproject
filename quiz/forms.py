from django import forms
from .models import Course, Question, Option


class QuizForm(forms.Form):
    course = forms.ModelChoiceField(
        queryset=Course.objects.all(),
        widget=forms.Select(attrs={
            'class': 'form-select form-select-lg',
            'aria-label': 'Select a course'
        })
    )
    number_of_questions = forms.IntegerField(
        min_value=1,
        widget=forms.NumberInput(attrs={
            'class': 'form-control form-control-lg',
            'placeholder': 'Number of questions'
        })
    )
    time_limit = forms.IntegerField(
        label="Time (minutes)",
        widget=forms.NumberInput(attrs={
            'class': 'form-control form-control-lg',
            'placeholder': 'Time in minutes'
        })
    )


def create_quiz_form(questions):
    """
    Dynamically create a form for answering quiz questions
    """
    class AnswerQuizForm(forms.Form):
        pass
    
    for question in questions:
        choices = [(option.id, option.option_text) for option in question.options.all()]
        
        field = forms.ChoiceField(
            label=question.question,
            choices=choices,
            widget=forms.RadioSelect(attrs={
                'class': 'form-check-input'
            }),
            required=True
        )
        AnswerQuizForm.base_fields[f'question_{question.id}'] = field
    
    return AnswerQuizForm()
