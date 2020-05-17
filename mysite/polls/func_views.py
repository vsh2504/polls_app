from django.shortcuts import render,get_object_or_404
from django.template import loader
from django.http import HttpResponse,HttpResponseRedirect
from django.urls import reverse
from .models import Question,Choice
from django.db.models import F

def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    context = {'latest_question_list': latest_question_list}
    return render(request, 'polls/index.html', context)
#detail 3
def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/detail.html', {'question': question})
#detail 2
# def detail(request, question_id):
#     try:
#         question = Question.object.get(pk=question_id)
#     except Question.DoesNotExist:
#         raise Http404("Question does not exist")
#     #return HttpResponse("You're looking at question %s." % question_id)

'''
 get_list_or_404() function, which works just as get_object_or_404() – except using filter() instead of get().
 It raises Http404 if the list is empty.
'''

def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/results.html', {'question': question})

#Vote View after voting
def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        # selected_choice.votes += 1
        selected_choice.votes = F('votes') + 1 #To avoid race conditions
        #if votes=42 and two user voted at same time then 43 will be saved insted of 44
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
