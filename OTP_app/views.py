from urllib import request
from django.shortcuts import render, redirect
from .forms import *
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from .models import Profile
import json
import random 
from django.conf import settings
from django.contrib.auth.hashers import make_password, check_password
import requests
# Create your views here.

def send_OTP(number, message):
    url = 'https://www.fast2sms.com/dev/bulkV2'
    my_data = {
    'sender_id': 'FSTSMS', 
    'message': message, 
    'language': 'english',
    'route': 'p',
    'numbers': number 
}
    headers = {
    'authorization': 'apikey',
    'Content-Type': "application/x-www-form-urlencoded",
    'Cache-Control': "no-cache"
}
    
    
    response = requests.request("POST",
                            url,
                            data = my_data,
                            headers = headers)
                            # load json data from source
    returned_msg = json.loads(response.text)
    print(returned_msg['message'])


def Registration(request):
    if request.method == 'POST' and 'registration' in request.POST:
        fm = UserRegistrationForm(request.POST)
        up = UserProfile(request.POST)
        if fm.is_valid() and up.is_valid():
            e = fm.cleaned_data['email']
            u = fm.cleaned_data['username']
            p = fm.cleaned_data['password1']
            request.session['email'] = e
            request.session['user'] = u
            request.session['password'] = p
            hashed_pwd = make_password(request.session['password'])
            p_number = up.cleaned_data['phone_number']
            request.session['number'] = p_number
            otp = random.randint(1000,9999)
            print(otp)
            print(p_number)
            request.session['otp'] = otp
            message = f"Your OTP is {otp}"
            send_OTP(p_number,message)
            return redirect('/registration/OTP/')
    else:
        fm = UserRegistrationForm()
        up = UserProfile()
    context = {'fm':fm, 'up':up}

    return render (request, 'registration.html',context)



def OTPRegistration(request):
    if request.method == 'POST' and 'otp-registration' in request.POST:
        u_otp = request.POST['otp']
        otp = request.session.get('otp')
        user = request.session.get('user')
        print(otp)
        hashed_pwd = make_password(request.session['password'])
        p_number = request.session.get('number')
        email_address = request.session.get('email')
        if int(u_otp)==otp:
            User.objects.create(username=user,email=email_address,password=hashed_pwd)
            user_instance = User.objects.get(username=user)
            Profile.objects.create(user=user_instance,phone_number=p_number)
            request.session.delete('otp')
            request.session.delete('user')
            request.session.delete('password')
            messages.success(request,'Registration Done!')
            return redirect('/login/')
        else:
            messages.error(request, 'Wrong OTP Try Again')

    return render (request, 'OTP_reg.html')


def UserLogin ( request ) :
    if request.method == "POST":
        username = request.POST['user']
        password = request.POST['password']
        user =authenticate(request ,username=username,password=password)
        if user is not None :
             request.session ['username'] = username
             request.session ['password'] = password
             u = User.objects.get(username = username) 
             p = Profile.objects.get(user=u)
             p_number = p.phone_number
             otp = random.randint ( 1000 , 9999 )
             request.session['login_otp'] = otp
             message =f'your otp is ( {otp})'
             send_OTP(p_number,message )
             return redirect('/login/otp/')
        else :
             messages.error(request,'username or password is wrong')
    return render(request ,'login.html' )

def otpLogin (request):
    if request.method == 'POST':
         username = request.session['username']
         password =  request.session['password']
         otp =  request.session.get('login_otp')
         u_otp = request.POST ['otp']
         if int (u_otp) == otp:
            user = authenticate(request , username =username , password = password )
            if user is not None :
                  login (request,user)
                  request.session.delete ('login_otp')
                  messages.success (request,'login successfully')
                  return redirect ('/')
            else:
                  messages.error(request,'Wrong OTP')
    return render ( request ,'login-otp.html')

def home(request) :
    return render ( request ,'home.html')