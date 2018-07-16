from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.utils import timezone
from .models import Todo
# Create your views here.


def index(request):
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
    todo = Todo.objects.get(id=id)
    template_name = 'detail.html'
    context = {'todo': todo}
    return render(request, 'details.html', context)


def update(request, id):
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
    if (request.method == 'POST'):
        title = request.POST['title']
        text = request.POST['text']
        column_id = request.POST['column_id']
        todo = Todo(title=title, text=text, column_id=column_id)
        todo.save()
        return redirect('/todos')
    else:
        return render(request, 'add.html')
