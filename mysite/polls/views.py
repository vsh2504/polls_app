#EARLIER FUNCTION BASED VIEWS IN func_views.py

from django.http import HttpResponseRedirect,JsonResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from .models import Choice, Question

'''
    Each generic view needs to know what model it will be acting upon.
    This is provided using the model attribute. The DetailView generic
    view expects the primary key value captured from the URL to be
    called "pk", so we’ve changed question_id to pk for the generic views.
'''
'''
    1. By default, the DetailView generic view uses a template
    called <app name>/<model name>_detail.html. eg. "polls/question_detail.html"
    2.the ListView generic view uses a default template called <app name>/<model name>_list.html.
'''

#for ListView, the automatically generated context variable is question_list.
class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    #ERROR:It shows polls in the future also and we need to make tests
    # def get_queryset(self):
    #     """Return the last five published questions."""
    #     return Question.objects.order_by('-pub_date')[:5]

    def get_queryset(self):
        """
        Return the last five published questions (not including those set to be
        published in the future).
        """
        return Question.objects.filter(
            pub_date__lte=timezone.now()
        ).order_by('-pub_date')[:5]

# For DetailView the question variable is provided automatically
# since we’re using a Django model (Question)
class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'

    #ERROR:Even though future questions don’t appear in the index,
    #users can still reach them if they know or guess the right URL.
    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Question.objects.filter(pub_date__lte=timezone.now())

class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'

    #ERROR:Even though future questions don’t appear in the index,
    #users can still reach them if they know or guess the right URL.
    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Question.objects.filter(pub_date__lte=timezone.now())

    #ADDING EXTRA CONTEXT DATA
    # def get_context_data(self, **kwargs):
    #     Call the base implementation first to get a context
    #     context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        # choice_list = []
        # choice_votes=[]
        # choiceSet = context['question'].choice_set.all()
        #
        # for choice in choiceSet:
        #     choice_list.append(choice.choice_text)
        #     choice_votes.append(choice.votes)
        #
        # context['choice_list'] = choice_list
        # context['choice_votes'] = choice_votes
        # context['choices'] = context['question'].choice_set.all()
        # return context

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
        selected_choice.votes += 1
        #selected_choice.votes = F('votes') + 1 #To avoid race conditions
        #if votes=42 and two user voted at same time then 43 will be saved insted of 44
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))

def resultsData(request,question_id):
    votedata = []

    question = Question.objects.get(id=question_id)
    choices = question.choice_set.all()

    for i in choices:
        votedata.append(
            {
                i.choice_text:i.votes
            }
        )
    print(votedata)
    return JsonResponse(votedata,safe=False)

def myMap(request):
    return render(request,'polls/maps_mapbox.html')
'''
**The Django test client
Django provides a test Client to simulate a user interacting with the
code at the view level. We can use it in tests.py or even in the shell.
'''
