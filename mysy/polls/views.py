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
from django.contrib.auth import authenticate, login, logout
from django import forms
from forms import UserRegForm, LoginForm

def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
#    output = ', '.join([p.question_text for p in latest_question_list])
#    return HttpResponse(output)
    template = loader.get_template('polls/index.html')
    context = RequestContext(request, {
        'latest_question_list': latest_question_list,
        'error': str(request.user),
    })
    return HttpResponse(template.render(context))

def detail(request, question_id):
    try:
        question = Question.objects.get(pk=question_id)
    except Question.DoesNotExist:
        raise Http404("Question does not exist")
    return render(request, 'polls/detail.html', {'question': question,'error':request.user})    


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
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user_name=request.POST["username"] 
            pass_word=request.POST["password"]
            user = authenticate(username=user_name, password=pass_word)
            if user is not None:
                if user.is_active:  
                    login(request, user)   
                    return HttpResponseRedirect(reverse('polls:index'))
                else:
                    template = loader.get_template('polls/user_login.html')
                    context = RequestContext(request, {
                        'login_info': 'The password is valid, but the account has been disabled!',
                        'form': form,
                    })
                    return HttpResponse(template.render(context)) 
            else:
                template = loader.get_template('polls/user_login.html')
                context = RequestContext(request, {
                   'login_info': 'The password is invalid!',
                   'form': form,
                })
                return HttpResponse(template.render(context))
        else:
            template = loader.get_template('polls/user_login.html')
            context = RequestContext(request, {
                'login_info': 'The form is invalid!',
                'form': form,
            }) 
            return HttpResponse(template.render(context))  
    else:
        form=LoginForm()
        template = loader.get_template('polls/user_login.html') 
        context = RequestContext(request, {
            'login_info': 'Please Authorize'+str(request.user),
            'form': form,
        }) 
        return HttpResponse(template.render(context))

def created_user(request):
    return render(request, 'polls/create_user.html', {})

def register(request):
    if request.method == 'POST': # If the form has been submitted... 
        # ContactForm was defined in the previous section 
        form = UserRegForm(request.POST) # A form bound to the POST data 
        if form.is_valid(): # All validation rules pass 
            # Process the data in form.cleaned_data 
            # ... 
            first_name=request.POST["first_name"]
            last_name= request.POST["last_name"] 
            user_name=request.POST["username"] 
            pass_word=request.POST["password"]  
            password2=request.POST["password2"] 
            emailid=request.POST["email"] 
            user = User.objects.filter(email=emailid).exists() 
            user1 = User.objects.filter(username=user_name).exists()  
            if user is False and user1 is False: 
                user = User.objects.create_user(user_name,emailid,pass_word) 
                user.last_name = last_name 
                user.first_name = first_name                            
                return HttpResponseRedirect(reverse('polls:created_user'))
            else:
                return render(request, 'polls/register.html', {'form':form, 'error_message':"Already Registered"},)
        else:
            return render(request, 'polls/register.html', {'form':form},)
    else:
        form=UserRegForm()
        return render(request, 'polls/register.html', {'form':form},)

def ulogout(request):
    logout(request)
    return HttpResponseRedirect(reverse('ulogin')) 

def create_user(request):
    first_name=request.POST["first_name"] 
    last_name= request.POST["last_name"]
    user_name=request.POST["username"]
    pass_word=request.POST["password"]
    password2=request.POST["password2"]
    emailid=request.POST["email"]
    user = User.objects.filter(email=emailid).exists()
    user1 = User.objects.filter(username=user_name).exists()
    if user is False and user1 is False:
        user = User.objects.create_user(user_name,emailid,pass_word)
        user.last_name = last_name
        user.first_name = first_name
        return HttpResponseRedirect(reverse('polls:created_user'))
    else:
#        return HttpResponseRedirect(reverse('ulogin', kwargs={ 'login_info': 'Account Already Exists, Please login with that username.', 'user': user, 'user1':user1 }))
        template = loader.get_template('polls/user_login.html') 
        context = RequestContext(request, { 
           'login_info': 'Account Already Exists, Please login with that username.',
        })
        return HttpResponse(template.render(context))
