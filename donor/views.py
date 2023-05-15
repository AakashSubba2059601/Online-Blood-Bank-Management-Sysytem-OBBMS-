from django.shortcuts import render,redirect,reverse
from . import forms,models
from django.db.models import Sum,Q
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect , HttpResponseBadRequest
from django.contrib.auth.decorators import login_required,user_passes_test
from django.conf import settings
from datetime import date, timedelta
from django.core.mail import send_mail
from django.contrib.auth.models import User
from blood import forms as bforms
from blood import models as bmodels
import random
from django.contrib import messages
from django.core.mail import EmailMessage
from django.conf import settings
from django.template.loader import render_to_string
import time
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.db.models import F
from datetime import timedelta
from django.utils import timezone
from datetime import timedelta
from django.utils import timezone



def donor_signup_view(request):
    userForm=forms.DonorUserForm()
    donorForm=forms.DonorForm()
    mydict={'userForm':userForm,'donorForm':donorForm}
    if request.method=='POST':
        userForm=forms.DonorUserForm(request.POST)
        donorForm=forms.DonorForm(request.POST,request.FILES)
        if userForm.is_valid() and donorForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            donor=donorForm.save(commit=False)
            donor.user=user
            donor.bloodgroup=donorForm.cleaned_data['bloodgroup']
            donor.save()
            subject = 'Welcome to Online Blood Bank Management System'
            message = 'Your account has been successfully Created. Click the link below to login:http://192.168.101.5:8000/donor/donorlogin'
            from_email = settings.EMAIL_HOST_USER
            to_list = userForm.cleaned_data.get('email')
            send_mail(subject, message, from_email, [to_list], fail_silently=True)
            messages.success(request,'Account Created Successfully')
            my_donor_group = Group.objects.get_or_create(name='DONOR')
            my_donor_group[0].user_set.add(user)
        return HttpResponseRedirect('donorlogin')
    return render(request,'donor/donorsignup.html',context=mydict)

def donor_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            if user.groups.filter(name='DONOR').exists():
                messages.success(request,'Login Successfully')
                login(request, user)
                return HttpResponseRedirect('donor-dashboard')
            else:
                # If the user is not in the donor group, show an error message
                messages.error(request, 'Invalid username or password')
        else:
            # If the user authentication fails, show an error message
            messages.error( request, 'Invalid username or password')
    else:
        messages.error(request,'')
    
    userForm = forms.DonorUserForm()
    return render(request, 'donor/donorlogin.html', {'form': userForm, 'message.error': messages.error})



def donorforgot(request):
    return render(request,'donor/donorforgot.html')

def send_otp(request):
    error_message = None
    #otp=random.randint(11111,99999)
    otp=int(time.strftime("%H%S%M")) +int(time.strftime("%S"))
    email = request.POST.get('email')
    user_email = models.Donor.objects.filter(email=email)
    if user_email:
        user = models.Donor.objects.get(email=email)
        user.otp = otp
        user.save()
        request.session['email']= request.POST['email']
        html_message = "Your One Time Password : - "+"" + str(otp)
        subject = "Welcome to Online Blood Bank Management System"
        email_from = settings.EMAIL_HOST_USER
        email_to=[email]
        message=EmailMessage(subject,html_message,email_from,email_to)
        message.send()
        messages.success(request,"OTP Sent Successfully To Your Email.")
        return redirect('enter_otp')
    else:
        messages.error(request,"Invalid Email Please Enter Correct Email.")
        return render(request, 'donor/donorforgot.html',{'error':error_message})
    
def enter_otp(request):
    error_message = None
    if request.session.has_key('email'):
        email = request.session['email']
        user = models.Donor.objects.filter(email=email)
        for u in user:
            user_otp = u.otp
        if request.method == "POST":
            otp = request.POST.get('otp')
            if not otp:
                error_message= "OTP is required"
            elif not user_otp == otp:
                error_message = "OTP is invalid"
            if not error_message:
                messages.success(request,"Successfully Entered Correct OTP.")
                return redirect("password_reset")
               
        return render(request, 'donor/enter_otp.html',{'error':error_message})

    else:
       return render(request,"donor/donorforgot.html")

from django.contrib.auth.hashers import make_password


from django.http import HttpResponse

from django.contrib.auth.hashers import check_password

def password_reset(request):
    error_message = None
    if request.session.has_key('email'):
        email = request.session['email']
        user = User.objects.get(email=email)
        if request.method == "POST":
            new_password = request.POST.get('newpassword')
            confirm_new_password = request.POST.get('confirmpassword')

            if not new_password:
                error_message = "Enter New Password"
            elif not confirm_new_password:
                error_message = "Enter New Confirm Password"
            elif new_password == user.password:
                error_message = "New password should be different from the old password"
            elif new_password != confirm_new_password:
                error_message = "Passwords do not match"
            elif check_password(new_password, user.password):
                error_message = "New password should be different from the old password"

            if not error_message:
                # assuming new_password is a plaintext password entered by the user
                hashed_password = make_password(new_password)
                # set the hashed password on the user object
                user.password = hashed_password

                # save the user object
                user.save()

                messages.success(request,"Password Changed Successfully")
                response = redirect("donorlogin")
                # add no-cache header to prevent caching of the page
                response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
                response['Pragma'] = 'no-cache'
                response['Expires'] = '0'
                return response

    return render(request,"donor/password_reset.html",{'error':error_message})

            
def donor_dashboard_view(request):
    donor= models.Donor.objects.filter(user_id=request.user.id).first()
    totalunit=models.User_Stock.objects.aggregate(Sum('unit'))
    dict={
        'A1':models.User_Stock.objects.filter(bloodgroup="A+").first(),
        'A2':models.User_Stock.objects.filter(bloodgroup="A-").first(),
        'B1':models.User_Stock.objects.filter(bloodgroup="B+").first(),
        'B2':models.User_Stock.objects.filter(bloodgroup="B-").first(),
        'AB1':models.User_Stock.objects.filter(bloodgroup="AB+").first(),
        'AB2':models.User_Stock.objects.filter(bloodgroup="AB-").first(),
        'O1':models.User_Stock.objects.filter(bloodgroup="O+").first(),
        'O2':models.User_Stock.objects.filter(bloodgroup="O-").first(),
        'totalbloodunit':totalunit['unit__sum'],
        'requestpending': bmodels.BloodRequest.objects.all().filter(request_by_donor=donor).filter(status='Pending').count(),
        'requestapproved': bmodels.BloodRequest.objects.all().filter(request_by_donor=donor).filter(status='Approved').count(),
        'requestmade': bmodels.BloodRequest.objects.all().filter(request_by_donor=donor).count(),
        'requestrejected': bmodels.BloodRequest.objects.all().filter(request_by_donor=donor).filter(status='Rejected').count(),
    }
    return render(request,'donor/donor_dashboard.html',context=dict)



def donate_blood_view(request):
    donor = models.Donor.objects.get(user_id=request.user.id)
    donation_form = forms.DonationForm()
    last_donation = donor.blooddonate_set.order_by('-date').first()
    if last_donation:
        last_donation_date = last_donation.date
        eligible_date = last_donation_date + timedelta(days=90)
        if last_donation.status != 'Approved':
            messages.error(request, "Your last donation is still pending approval.")
            return HttpResponseRedirect('donation-history')
        elif timezone.now().date() < eligible_date:
            messages.error(request, "You can donate blood only after {}".format(eligible_date))
            return HttpResponseRedirect('donation-history')

    if request.method == 'POST':
        donation_form = forms.DonationForm(request.POST)
        if donation_form.is_valid():
            blood_donate = donation_form.save(commit=False)
            blood_donate.bloodgroup = donation_form.cleaned_data['bloodgroup']
            donor = models.Donor.objects.get(user_id=request.user.id)
            blood_donate.donor = donor
            blood_donate.save()
            # Update the corresponding stock of the blood group
            stock = models.User_Stock.objects.filter(bloodgroup=blood_donate.bloodgroup).first()
            if stock:
                stock.unit = F('unit') + blood_donate.unit
                stock.save()
            else:
                models.User_Stock.objects.create(bloodgroup=blood_donate.bloodgroup, unit=blood_donate.unit)


            messages.success(request, "Your donation request has been submitted for approval.")
            return HttpResponseRedirect('donation-history')
        else:
            messages.error(request, "Invalid fields! Please try again.")

    return render(request, 'donor/donate_blood.html', {'donation_form': donation_form})


def donation_history_view(request):
    donor= models.Donor.objects.get(user_id=request.user.id)
    donations=models.BloodDonate.objects.all().filter(donor=donor)
    return render(request,'donor/donation_history.html',{'donations':donations})

def make_request_view(request):
    request_form=bforms.RequestForm()
    if request.method=='POST':
        request_form=bforms.RequestForm(request.POST)
        if request_form.is_valid():
            blood_request=request_form.save(commit=False)
            blood_request.bloodgroup=request_form.cleaned_data['bloodgroup']
            donor= models.Donor.objects.get(user_id=request.user.id)
            blood_request.request_by_donor=donor
            blood_request.save()
            messages.success(request,"Successfully request")
            return HttpResponseRedirect('request-history')
        else:
            messages.error(request,"Invalid fields! Please try again.")
  
    return render(request,'donor/makerequest.html',{'request_form':request_form})

def request_history_view(request):
    donor= models.Donor.objects.get(user_id=request.user.id)
    blood_request=bmodels.BloodRequest.objects.all().filter(request_by_donor=donor)
    return render(request,'donor/request_history.html',{'blood_request':blood_request})

def donor_update_view(request,pk):
    donor=models.Donor.objects.get(id=pk)
    user=models.User.objects.get(id=donor.user_id)
    userForm=forms.DonorUserForm(instance=user)
    donorForm=forms.DonorForm(request.FILES,instance=donor)
    mydict={'userForm':userForm,'donorForm':donorForm}
    if request.method=='POST':
        userForm=forms.DonorUserForm(request.POST,instance=user)
        donorForm=forms.DonorForm(request.POST,request.FILES,instance=donor)
        if userForm.is_valid() and donorForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            donor=donorForm.save(commit=False)
            donor.user=user
            donor.bloodgroup=donorForm.cleaned_data['bloodgroup']
            donor.save()
            return redirect('donor-dashboard')
    return render(request,'donor/donor_update.html',context=mydict)

from donor.models import Contact
def contact(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        content = request.POST.get('content')
        
        if name and email and phone and content:  # check if all fields are filled
            contact = Contact(name=name, email=email, phone=phone, content=content)
            contact.save()
            messages.success(request, "Successfully messaged Admin.")
            return redirect('contact')
        else:
            messages.error(request, "Please fill all fields to message.")
    
    return render(request, "donor/Contact_us.html")

def image(request):
    return render(request,'donor/image.html')






