#from django.shortcuts import render
from django.http import HttpResponse
from django.http import Http404
from django.shortcuts import render
# Create your views here.
from polls.models import Question
from django.template import RequestContext, loader
from django.core.mail import send_mail

def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
#    output = ', '.join([p.question_text for p in latest_question_list])
#    return HttpResponse(output)
    template = loader.get_template('polls/index.html')
    context = RequestContext(request, {
        'latest_question_list': latest_question_list,
    })
    send_mail('iSmile Please', 'Here is the message.', 'norply@mysy.com',     ['pankaj.anand.26@gmail.com','pankaj_anand_26@yahoo.co.in'], fail_silently=False)
    return HttpResponse(template.render(context))

def detail(request, question_id):
#    response = "You're looking at the results of question %s."
#    return HttpResponse(response % question_id)
    try:
        question = Question.objects.get(pk=question_id)
    except Question.DoesNotExist:
        raise Http404("Question does not exist")
    return render(request, 'polls/detail.html', {'question': question})    


def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id) 
    return render(request, 'polls/results.html', {'question': question})    

response = "You're looking at the results of question %s."
    return HttpResponse(response % question_id)

def vote(request, question_id):
    p = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = p.choice_set.get(pk=request.POST['choice'])
    except KeyError, Choice.DoesNotExist):
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

