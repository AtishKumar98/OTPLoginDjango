from django.urls import path
from . import views

urlpatterns = [
    path('',views.home, name= 'home'),
    path('registration/',views.Registration, name= 'Registration'),
    path('registration/OTP/',views.OTPRegistration, name= 'RegistrationOTP'),
    path('login/',views.UserLogin, name= 'login'),
    path('login/otp/',views.otpLogin, name= 'otp-login'),
]
