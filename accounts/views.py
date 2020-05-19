from django.shortcuts import render, redirect
from .forms import CreateUserForm, ProfileForm
from django.contrib.auth import authenticate, login, logout

from django.contrib.auth.decorators import login_required


def register_user(request):
    form = CreateUserForm
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('product')
    context = {'form': form}
    return render(request, 'accounts/register.html', context)


def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('product')
    return render(request, 'accounts/login.html')


def logout_user(request):
    logout(request)
    return redirect('product')


@login_required(login_url='login')
def profile(request):
    profile = request.user.profile
    form = ProfileForm(instance=profile)
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
    context = {'form': form}
    return render(request, 'accounts/profile.html', context)