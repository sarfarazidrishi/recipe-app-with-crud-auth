from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.urls import reverse
from django.contrib import messages

# Create your views here.

errors={} #create empty dictnory to store and show errors 
def login(request):
    if request.method == 'POST':
        username= request.POST.get('username')
        password= request.POST.get('password')

        userauth=auth.authenticate(username=username, password=password)
        if userauth is not None:
            auth.login(request, userauth)
            return redirect('/')
        else:
            errors['userNOT_exists']='invalid credentials'
            return render(request, 'login.html', {'errors':errors})
    else:
        return render(request, 'login.html')

def register(request):
    if request.method == 'POST':
        userDetails = request.POST
        profileimg = request.FILES.get('profileimg')
        first_name = userDetails.get('first_name')
        last_name = userDetails.get('last_name')
        username= userDetails.get('username')
        email = userDetails.get('email')
        password = userDetails.get('password')
        confirm_password = userDetails.get('confirm_password')

        errors={} #create empty dictnory

        if password==confirm_password:
            if User.objects.filter(username=username).exists():
                errors['username_error']='username exists'
                # messages.info(request, "username exists")
                return render(request, 'register.html', {'errors':errors})
            elif User.objects.filter(email=email).exists():
                errors['email_error']='email exists , use another email'
                # messages.info(request, "email exists , use another email")
                return render(request, 'register.html', {'errors':errors})
            else:
               user= User.objects.create_user(
                   profileimg=profileimg,
                   username=username,
                   password=password, 
                   first_name=first_name, 
                   last_name=last_name, 
                   email=email,)
               user.save()
            #    messages.info(request, "user created")
            return redirect(reverse('accounts:login'))
        else:
            errors['password_error']='password sahi nhi h'
            # messages.info(request, 'password sahi nhi h')
        return render(request, 'register.html', {'errors':errors})
    else:
      return render(request, 'register.html')
    
def logout(request):
    auth.logout(request)
    return redirect('/')