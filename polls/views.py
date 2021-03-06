from django.shortcuts import render,get_object_or_404,reverse
from django.http import HttpResponse,HttpResponseRedirect
from .models import Question,Choice

# Create your views here.
def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    #output = ', '.join([question.question_text for question in latest_question_list])
    #return HttpResponse(output)
    context = {'latest_question_list': latest_question_list}
    return render(request, 'polls/index.html', context)    

def detail(request, question_id):
    #return HttpResponse('You are looking at question {}'.format(question_id))
    question = get_object_or_404(Question, id=question_id)
    return render(request, 'polls/detail.html',{'question':question})

def results(request, question_id):
	question = get_object_or_404(Question, pk=question_id)
	return render(request, 'polls/results.html',{'question':question})

#def vote(request, question_id):
   # return HttpResponse('You are voting on question {}'.format(question_id))	
def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    if request.method == 'POST':
        choice_id = request.POST.get('choice',0)
        try:
            #selected_choice = question.choice_set.get(pk=request.POST['choice'])
            selected_choice = question.choice_set.get(pk=choice_id)
        except (KeyError, Choice.DoesNotExist):
            # Redisplay the question voting form.
            return render(request, 'polls/detail.html', {
                'question': question,
                'error_message': "You didn't select a choice.",
            })
        else:
            selected_choice.votes += 1
            selected_choice.save()
            # Always return an HttpResponseRedirect after successfully dealing
            # with POST data. This prevents data from being posted twice if a
            # user hits the Back button.
            return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
            #return HttpResponseRedirect('https://www.google.com')
    else:
        return HttpResponse('Your post question id:%s' % question.id)
