from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Question, Result
from .forms import RegisterForm
import random

@login_required
def start_exam(request):

    if request.method == 'POST':
        question_ids = request.session.get('question_ids')
        questions = Question.objects.filter(id__in=question_ids)

        score = 0
        for q in questions:
            selected = request.POST.get(str(q.id))
            if selected == q.correct_answer:
                score += 1

        Result.objects.create(student=request.user, score=score)
        return render(request, 'exam/result.html', {'score': score,'questions': questions})

    else:
        questions = list(Question.objects.all())
        random.shuffle(questions)
        questions = questions[:5]

        # store IDs in session
        request.session['question_ids'] = [q.id for q in questions]

    return render(request, 'exam/exam.html', {'questions': questions})

def register_view(request):
    form = RegisterForm(request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)
        user.set_password(form.cleaned_data['password'])
        user.save()
        return redirect('login')
    return render(request, 'exam/register.html', {'form': form})

@login_required
def result_history(request):
    results = Result.objects.filter(student=request.user).order_by('-date')
    return render(request, 'exam/history.html', {'results': results})
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('dashboard')
    return render(request, 'exam/login.html')


@login_required
def dashboard(request):
    return render(request, 'exam/dashboards.html')


@login_required
def start_exam(request):
    questions = Question.objects.order_by('?')[:5]
    if request.method == 'POST':
        score = 0
        for q in questions:
            selected = request.POST.get(str(q.id))
            if selected == q.correct_answer:
                score += 1

        Result.objects.create(student=request.user, score=score)
        return render(request, 'exam/result.html', {'score': score,'questions': questions})

    return render(request, 'exam/exam.html', {'questions': questions})


def logout_view(request):
    logout(request)
    return redirect('login')