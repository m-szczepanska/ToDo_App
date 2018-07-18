from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.http import HttpResponse

from .models import User


# TODO: Login error how
# TODO: Update all urls so that login page is first
# TODO: Fix the login template location
#       (it's in /templates, not in /users/templates)
def login_view(request):
    if(request.method == 'POST'):
        user_name = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=user_name, password=password)
        if user is not None:
            login(request, user)
            return redirect('/todos')
        else:
            return render(request, 'login.html')
    else:
        return render(request, 'login.html')

    #     try:
    #         user = User.objects.get(username=user_name)
    #     except User.DoesNotExist:
    #         return render(request, 'login.html')
    #     if user.check_password(password):
    #         login(request, user)
    #         return redirect('/todos')
    #     else:
    #         return render(request, 'login.html')
    # else:
    #     return render(request, 'login.html')


def logout_view(request):
    logout(request)
    return render(request, 'login.html')
