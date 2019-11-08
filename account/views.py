from django.shortcuts import render, redirect
from django.contrib.auth import login,authenticate,logout
from django.contrib.auth.decorators import login_required
from random import randint

from .models import Account
from .forms import RegistrationForm, LoginForm, UpdateForm

def registration_view(request):
    if request.user.is_authenticated:
        return redirect('books:home')
    context = {}
    if request.POST:
        formreg = RegistrationForm(request.POST, request.FILES)
        if formreg.is_valid():
            formreg.save()
            email = formreg.cleaned_data.get('email')
            paswd = formreg.cleaned_data.get('password1')
            user = authenticate(username=email, password=paswd)
            if user:
                login(request, user)
                if 'next' in request.POST:
                    return redirect(request.POST['next'])
                return redirect('books:home')
            else:
                context['formreg'] = formreg
                context['formlogin'] = LoginForm()
                context['login'] = False
                return render(request, 'account/registration.html', context=context)
        else:
            context['formreg'] = formreg
            context['formlogin'] = LoginForm()
            context['login'] = False
            return render(request, 'account/registration.html', context=context)
    else:
        context['formreg'] = RegistrationForm()
        context['formlogin'] = LoginForm()
        context['login'] = False
        return render(request, 'account/registration.html', context=context)

@login_required
def logout_view(request):
    if not request.user.is_authenticated:
        return redirect('account:login')
    logout(request)
    return redirect('books:home')


def login_view(request,next='/'):

    formlogin = LoginForm()

    if request.user.is_authenticated:
        return redirect('books:home')

    if request.POST:
        formlogin = LoginForm(request.POST)
        if formlogin.is_valid():
            email = request.POST['email']
            paswd = request.POST['password']
            user = authenticate(username=email, password=paswd)
            if user:
                login(request, user)
                if request.POST.get('next'):
                    print('yesss')
                    return redirect(request.POST['next'])
                return redirect('books:home')
    print(next)
    if request.GET.get('next'):
        next = request.GET.get('next')
    return render(request, 'account/login1.html', context={
        'formlogin' : formlogin,
        'formreg' : RegistrationForm(),
        'login' : True,
        'next' : next,
    })

def profilepage(request):
    context = {}
    context['']

@login_required
def update_view(request):

    form = UpdateForm(initial= {
        'email':request.user.email,
        'username':request.user.username,
        'dob':request.user.dob,
    })
    context = {}
    context['auth'] = True
    context['edit'] = False
    if not request.user.is_authenticated:
        return redirect('account:login')

    if request.POST:
        form = UpdateForm(request.POST, request.FILES, instance=request.user)
        context['edit'] = True
        if form.is_valid():
            form.save()
            context['edit'] = False
        else:
            context['edit'] = True
    context['form'] = form
    return render(request, 'account/update.html', context)
