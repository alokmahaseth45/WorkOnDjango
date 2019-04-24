from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.messages import constants as messages
from django.contrib.auth import views

# from .forms import Signupform, Loginform
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login

# from django.contrib.auth.views import login



from home.form import SignUpForm
# from home.form import NewUserForm,SignUpForm





def index(request):
    # return HttpResponse("<h1>This is the home page</h1>")
    return render(request, 'base.html')

def logout_request(request):
    logout(request)
    messages.info(request, "Logged out successfully!")
    return redirect("main:homepage")



def login_request(request):
    if request.method == 'POST':
        form = AuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                context = {'form': form,
                           'error': 'The login has been successful'}
                # views.login(request, user)
                # messages.info(request, f"You are now logged in as {username}")
                # return redirect('/')
                return render(request, 'base.html', {'name' : request.user.username })
            else:
                context = {'form': form,
                           'error': 'The username and password combination is incorrect'}

                # messages.error(request, "Invalid username or password.")
        else:
            context = {'form': form}
            return render(request, 'siteusers/login.html', context)
            # messages.error(request, "Invalid username or password.")
    form = AuthenticationForm()
    return render(request = request,
                    template_name = "login.html",
                    context={"form":form})



def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})