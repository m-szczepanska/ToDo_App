import time
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.http import HttpResponse

from users.models import User, PasswordResetToken, CreateAccountToken
from users.services import send_password_reset_mail
from users.user_register_services import send_user_register_mail
from users.password_validator import MinimumLengthValidator, NumericPasswordValidator


def login_view(request):
    if(request.method == 'POST'):
        user_name = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=user_name, password=password)
        if user is not None:
            login(request, user)
            return redirect('/todos')
        else:
            context = {"error": "Login or password incorrect"}
            return render(request, 'login.html', context)
    else:
        return render(request, 'login.html')


def logout_view(request):
    logout(request)
    return render(request, 'login.html')


def register_request_view(request):
    if(request.method == 'POST'):
        user_email = request.POST['user_email']
        try:
            user = User.objects.get(email=user_email)
            error = "Given email adress is already in database."
            context = {"error": error}
            return render(request, 'register_request.html', context)
        except:
            token = CreateAccountToken()
            token.save()
            send_user_register_mail(user_email, token.uuid)
            reset_correct_message = (
                "A link to register has been sent to the e-mail address "
                "you entered."
            )
            context = {"message": reset_correct_message}
            return render(request, 'register_request.html', context)
    else:
        return render(request, 'register_request.html')



def password_reset_request_view(request):
    if(request.method == 'POST'):
        user_email = request.POST['user_email']
        try:
            user = User.objects.get(email=user_email)
        except:
            error = "Given email adress is not registered in database."
            context = {"error": error}
            return render(request, 'password_reset_request.html', context)

        token = PasswordResetToken(user=user)
        token.save()
        send_password_reset_mail(user_email, token.uuid)
        reset_correct_message = (
            "A link to reset your password has been sent to the e-mail address "
            "you entered."
        )
        context = {"message": reset_correct_message}
        return render(request, 'password_reset_request.html', context)
    else:
        return render(request, 'password_reset_request.html')


def password_reset_view(request):
    # Fail if request doesn't have data that we need
    # Check if querystring has a 'token' (bad: t=1234-5678-9999)

    if(request.method == 'POST'):
        # Ugly hack; browser always adds / at end of token
        token_uuid = request.POST.get('token', ' ')[:-1]
        if not token_uuid:
            return HttpResponse(status=400)

        # Check if token is in db (bad: user tried to hack and typed their own
        # token)
        try:
            token = PasswordResetToken.objects.get(uuid=token_uuid)
        except:
            context = {"error": "Invalid token"}
            return render(request, 'password_reset_request.html', context)

        # Check if token is valid
        if not token.is_valid:
            context = {"error": "Token expired"}
            return render(request, 'password_reset_request.html', context)

        password_1 = request.POST['password_1']
        password_2 = request.POST['password_2']

        if password_1 != password_2:
            context = {"error": "Passwords didn't match"}
            return render(request, 'password_reset.html', context)

        if MinimumLengthValidator.validate(password_1):
            if NumericPasswordValidator.validate(password_1):
                token.user.set_password(password_1)
                token.user.save()
                token.was_used = True
                token.save()
                context = {"message": "Password successfully changed"}
                return render(request, 'login.html', context)
            else:
                context = {"error": "Password must contain at least 1 digit"}
                return render(request, 'password_reset.html', context)
        else:
            context = {"error": "Passwords must have at least 8 characters"}
            return render(request, 'password_reset.html', context)

    else:
        token_uuid = request.GET.get('token')
        if not token_uuid:
            return HttpResponse(status=400)

        # Check if token is in db (bad: user tried to hack and typed their own
        # token)
        try:
            token = PasswordResetToken.objects.get(uuid=token_uuid)
        except:
            context = {"error": "Invalid token"}
            return render(request, 'password_reset_request.html', context)

        # Check if token is valid
        if not token.is_valid:
            context = {"error": "Token expired"}
            return render(request, 'password_reset_request.html', context)

        return render(request, 'password_reset.html')



def register_view(request):
    # Fail if request doesn't have data that we need
    # Check if querystring has a 'token' (bad: t=1234-5678-9999)

    if(request.method == 'POST'):
        # Ugly hack; browser always adds / at end of token
        token_uuid = request.POST.get('token', ' ')[:-1]
        if not token_uuid:
            return HttpResponse(status=400)

        # Check if token is in db (bad: user tried to hack and typed their own
        # token)
        try:
            token = CreateAccountToken.objects.get(uuid=token_uuid)
        except:
            context = {"error": "Invalid token"}
            return render(request, 'register_request.html', context)

        # Check if token is valid
        if not token.is_valid:
            context = {"error": "Token expired"}
            return render(request, 'register_request.html', context)

        user_email = request.POST['user_email']
        try:
            user = User.objects.get(email=user_email)
            error = "Given email adress is already in database."
            context = {"error": error}
            return render(request, 'register.html', context)
        except:
            username = request.POST['username']
            try:
                user = User.objects.get(username=username)
                error = "Given username adress is already in database."
                context = {"error": error}
                return render(request, 'register.html', context)
            except:
                user = User.objects.create_user(username=username, email=user_email)
                # user.save()

        password_1 = request.POST['password_1']
        password_2 = request.POST['password_2']

        if password_1 != password_2:
            context = {"error": "Passwords didn't match"}
            return render(request, 'register.html', context)

        if MinimumLengthValidator.validate(password_1):
            if NumericPasswordValidator.validate(password_1):
                user.set_password(password_1)
                user.save()
                token.was_used = True
                token.save()
                context = {"message": "Your account has been created"}
                return render(request, 'login.html', context)
            else:
                context = {"error": "Password must contain at least 1 digit"}
                return render(request, 'register.html', context)
        else:
            context = {"error": "Passwords must have at least 8 characters"}
            return render(request, 'register.html', context)

    else:
        token_uuid = request.GET.get('token')
        if not token_uuid:
            return HttpResponse(status=400)

        try:
            token = CreateAccountToken.objects.get(uuid=token_uuid)
        except:
            context = {"error": "Very Invalid token"}
            return render(request, 'register_request.html', context)

        if not token.is_valid:
            context = {"error": "Token expired"}
            return render(request, 'register_request.html', context)

        return render(request, 'register.html')
