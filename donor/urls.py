from django.urls import path
from django.contrib.auth.views import LoginView
from . import views
from donor.views import *


urlpatterns = [
    path('donorlogin', views.donor_login, name='donorlogin'),
    path('donorsignup', views.donor_signup_view, name='donorsignup'),
    path('donor-dashboard', views.donor_dashboard_view, name='donor-dashboard'),
    path('donate-blood', views.donate_blood_view, name='donate-blood'),
    path('donation-history', views.donation_history_view, name='donation-history'),
    path('make-request', views.make_request_view, name='make-request'),
    path('request-history', views.request_history_view, name='request-history'),
    path('donorforgot', views.donorforgot, name='donorforgot'),
    path('send_otp', views.send_otp, name='send_otp'),
    path('enter_otp', views.enter_otp, name='enter_otp'),
    path('password_reset', views.password_reset, name='password_reset'),
    path('contact', views.contact, name='contact'),
    path('image', views.image, name='image'),

]
