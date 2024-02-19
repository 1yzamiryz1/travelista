import re

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q
from django.shortcuts import render, redirect, reverse

from accounts.forms import CustomUserCreationForm, CustomAuthenticationForm


def is_valid_email(email):
    email_regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    return re.match(email_regex, email)


def email_to_username(email):
    try:
        user = User.objects.get(email=email)
        return user.username
    except User.DoesNotExist:
        return None


def login_view(request):
    if not request.user.is_authenticated:
        if request.method == "POST":
            form = CustomAuthenticationForm(request=request, data=request.POST.copy())
            login_data = form.data.get('username')
            is_email = is_valid_email(login_data)

            if is_email:
                username_from_email = email_to_username(login_data)
                if username_from_email:
                    form.data['username'] = username_from_email

            if form.is_valid():
                login_data = form.cleaned_data.get('username')
                password = form.cleaned_data.get('password')
                user = authenticate(request, username=login_data, password=password)

                if user is not None:
                    login(request, user)
                    messages.add_message(request, messages.SUCCESS, f'{login_data} logged in successfully')
                    return redirect(reverse('website:index_view'))
                else:
                    messages.add_message(request, messages.ERROR, "Sorry, we couldn't log you in")
                    return redirect(reverse('website:index_view'))
        else:
            form = CustomAuthenticationForm()
        context = {'form': form}
        return render(request, 'accounts/login.html', context)
    else:
        return redirect(reverse('website:index_view'))


@login_required
def logout_view(request):
    logout(request)
    messages.add_message(request, messages.SUCCESS, 'Logged Out Successfully')
    return redirect(reverse('website:index_view'))


def is_user_exists(email, username):
    return User.objects.filter(Q(email=email) | Q(username=username)).exists()


def signup_view(request):
    if not request.user.is_authenticated:
        if request.method == "POST":
            email = request.POST.get('email')
            username = request.POST.get('username')
            password1 = request.POST.get('password1')
            password2 = request.POST.get('password2')

            if not is_valid_email(email):
                messages.add_message(request, messages.ERROR, 'Please enter a valid email address.')
                return redirect('accounts:signup')

            if is_user_exists(email, username):
                messages.add_message(request, messages.ERROR, 'This email or username is already in use.')
                return redirect('accounts:signup')

            form = CustomUserCreationForm({
                'username': username,
                'email': email,
                'password1': password1,
                'password2': password2,
            })

            if form.is_valid():
                form.save()
                messages.add_message(request, messages.SUCCESS, 'User created Successfully')
                return redirect('accounts:login')
            else:
                messages.add_message(request, messages.ERROR, 'Sorry Something went wrong')

        else:
            form = CustomUserCreationForm()

        context = {'form': form}
        return render(request, 'accounts/signup.html', context)
    else:
        return redirect(reverse('website:index_view'))
