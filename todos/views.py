from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.utils import timezone
from .models import Todo
# Create your views here.


def index(request):
    user_id = request.user.id
    if not user_id:
        return HttpResponseRedirect(reverse('login'))

    left = Todo.objects.filter(column_id='left')#.order_by(-'updated_at')
    middle = Todo.objects.filter(column_id='middle')
    right = Todo.objects.filter(column_id='right')
    context = {
        'left': left,
        'middle': middle,
        'right': right
    }
    return render(request, 'index.html', context)


def details(request, id):
    user_id = request.user.id
    if not user_id:
        return HttpResponseRedirect(reverse('login'))

    todo = Todo.objects.get(id=id)
    template_name = 'detail.html'
    context = {'todo': todo}
    return render(request, 'details.html', context)


def update(request, id):
    user_id = request.user.id
    if not user_id:
        return HttpResponseRedirect(reverse('login'))

    # TODO: This should be a PUT
    query_string = request.GET.urlencode()
    # Fail if request doesn't have data that we need
    if 'column_id' not in query_string:
        return HttpResponse(status=400)
    column_id = query_string.split('=')[1]
    # Only three values available now
    if column_id not in ['left', 'middle', 'right']:
        return HttpResponse(status=400)

    todo = Todo.objects.get(id=id)
    todo.column_id = column_id
    todo.save()
    return HttpResponse(status=204)


def add(request):
    user_id = request.user.id
    if not user_id:
        return HttpResponseRedirect(reverse('login'))

    if (request.method == 'POST'):
        title = request.POST['title']
        text = request.POST['text']
        column_id = request.POST['column_id']
        todo = Todo(title=title, text=text, column_id=column_id)
        todo.save()
        return redirect('/todos')
    else:
        return render(request, 'add.html')
