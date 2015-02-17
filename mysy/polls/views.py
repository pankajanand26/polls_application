#from django.shortcuts import render
from django import forms
from django.http import HttpResponse, HttpResponseRedirect
from django.http import Http404
from django.shortcuts import render
# Create your views here.
from polls.models import Question
from django.template import RequestContext, loader
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, render
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
#    output = ', '.join([p.question_text for p in latest_question_list])
#    return HttpResponse(output)
    template = loader.get_template('polls/index.html')
    context = RequestContext(request, {
        'latest_question_list': latest_question_list,
    })
    return HttpResponse(template.render(context))

def detail(request, question_id):
    try:
        question = Question.objects.get(pk=question_id)
    except Question.DoesNotExist:
        raise Http404("Question does not exist")
    return render(request, 'polls/detail.html', {'question': question})    


def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id) 
    return render(request, 'polls/results.html', {'question': question})    


def vote(request, question_id):
    p = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = p.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'polls/detail.html', { 
            'question': p, 
            'error_message': "You didn't select a choice.", 
        }) 
    else: 
        selected_choice.votes += 1 
        selected_choice.save() 
        # Always return an HttpResponseRedirect after successfully dealing 
        # with POST data. This prevents data from being posted twice if a 
        # user hits the Back button. 
        return HttpResponseRedirect(reverse('polls:results', args=(p.id,)))

def ulogin(request): 
    template = loader.get_template('polls/user_login.html') 
    context = RequestContext(request, { 
    }) 
    return HttpResponse(template.render(context))

def created_user(request):
    return render(request, 'polls/create_user.html', {})

def register(request):
    return render(request, 'polls/register.html', {})

def create_user(request):
    first_name=request.POST["first_name"] 
    last_name= request.POST["last_name"]
    user_name=request.POST["username"]
    pass_word=request.POST["pass"]
    emailid=request.POST["email"]
    user = User.objects.filter(email=emailid).exists()
    if user is None:
        user = User.objects.create_user(user_name,emailid,pass_word)
        user.last_name = last_name
        user.first_name = first_name
        return HttpResponseRedirect(reverse('polls:created_user'))
    else:
        return HttpResponseRedirect(reverse('ulogin'))
