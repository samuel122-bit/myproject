from django.shortcuts import render
import random
from .models import Question, Option
from .forms import QuizForm, create_quiz_form


def home(request):
    form = QuizForm()
    if request.method == "POST":
        form = QuizForm(request.POST)
        if form.is_valid():
            course = form.cleaned_data['course']
            number = form.cleaned_data['number_of_questions']
            time = form.cleaned_data['time_limit']
            avalible = Question.objects.filter(course=course).count()
            if number > avalible:
                form.add_error("number_of_questions", f"Only {avalible} questions are avaliable for {course.name}. please choose a number between 1 and {avalible}")
                return render(request, "home.html", {"form": form})
            questions = list(Question.objects.filter(course=course))
            random.shuffle(questions)
            questions = questions[:number]
            request.session['time'] = time
            quiz_form = create_quiz_form(questions)
            return render(request, "quiz.html", {"questions": questions, "time": time, "quiz_form": quiz_form})
        else:
            form = QuizForm()
    return render(request, "home.html", {"form": form})

def result(request):
    score = 0
    total = 0
    for key, value in request.POST.items():
        if key == "csrfmiddlewaretoken":
            continue
        total = total + 1
        option = Option.objects.get(id=value)
        if option.is_correct:
            score = score + 1
    
    # Calculate performance level
    if total == 0:
        percentage = 0
        performance = "unknown"
    else:
        percentage = (score / total) * 100
        if score == total:
            performance = "perfect"
        elif percentage >= 80:
            performance = "great"
        elif percentage >= 60:
            performance = "good"
        else:
            performance = "keep_learning"
    
    context = {
        "score": score,
        "total": total,
        "percentage": round(percentage),
        "performance": performance
    }
    return render(request, "result.html", context)
