from django.shortcuts import render,redirect,reverse
from . import forms,models
from django.db.models import Sum,Q
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required,user_passes_test
from django.conf import settings
from datetime import date, timedelta
from django.core.mail import send_mail
from django.contrib.auth.models import User
from donor import models as dmodels
from patient import models as pmodels
from donor import forms as dforms
from patient import forms as pforms
from django.shortcuts import render, redirect
import csv
from django.http import HttpResponse
from django.urls import reverse
from django.utils.text import slugify
from django.contrib import messages




def home_view(request):
    x=models.Stock.objects.all()
    print(x)
    if len(x)==0:
        blood1=models.Stock()
        blood1.bloodgroup="A+"
        blood1.save()

        blood2=models.Stock()
        blood2.bloodgroup="A-"
        blood2.save()

        blood3=models.Stock()
        blood3.bloodgroup="B+"
        blood3.save()        

        blood4=models.Stock()
        blood4.bloodgroup="B-"
        blood4.save()

        blood5=models.Stock()
        blood5.bloodgroup="AB+"
        blood5.save()

        blood6=models.Stock()
        blood6.bloodgroup="AB-"
        blood6.save()

        blood7=models.Stock()
        blood7.bloodgroup="O+"
        blood7.save()

        blood8=models.Stock()
        blood8.bloodgroup="O-"
        blood8.save()

    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')  
    return render(request,'blood/index.html')

def is_donor(user):
    return user.groups.filter(name='DONOR').exists()

def is_patient(user):
    return user.groups.filter(name='PATIENT').exists()


def afterlogin_view(request):
    if is_donor(request.user):      
        return redirect('donor/donor-dashboard')
                
    elif is_patient(request.user):
        return redirect('patient/patient-dashboard')
    else:
        return redirect('admin-dashboard')

@login_required(login_url='adminlogin')
def admin_dashboard_view(request):
    totalunit = models.Stock.objects.aggregate(Sum('unit'))
    dict = {
        'A1': models.Stock.objects.filter(bloodgroup="A+").order_by('-unit').first(),
        'A2': models.Stock.objects.filter(bloodgroup="A-").order_by('-unit').first(),
        'B1': models.Stock.objects.filter(bloodgroup="B+").order_by('-unit').first(),
        'B2': models.Stock.objects.filter(bloodgroup="B-").order_by('-unit').first(),
        'AB1': models.Stock.objects.filter(bloodgroup="AB+").order_by('-unit').first(),
        'AB2': models.Stock.objects.filter(bloodgroup="AB-").order_by('-unit').first(),
        'O1': models.Stock.objects.filter(bloodgroup="O+").order_by('-unit').first(),
        'O2': models.Stock.objects.filter(bloodgroup="O-").order_by('-unit').first(),
        'totaldonors': dmodels.Donor.objects.all().count(),
        'totalbloodunit': totalunit['unit__sum'],
        'totalrequest': models.BloodRequest.objects.all().count(),
        'totalapprovedrequest': models.BloodRequest.objects.filter(status='Approved').count()
    }
    return render(request, 'blood/admin_dashboard.html', context=dict)

@login_required(login_url='adminlogin')
def admin_blood_view(request):
    dict={
        'bloodForm':forms.BloodForm(),
        'A1':models.Stock.objects.get(bloodgroup="A+"),
        'A2':models.Stock.objects.get(bloodgroup="A-"),
        'B1':models.Stock.objects.get(bloodgroup="B+"),
        'B2':models.Stock.objects.get(bloodgroup="B-"),
        'AB1':models.Stock.objects.get(bloodgroup="AB+"),
        'AB2':models.Stock.objects.get(bloodgroup="AB-"),
        'O1':models.Stock.objects.get(bloodgroup="O+"),
        'O2':models.Stock.objects.get(bloodgroup="O-"),
    }
    if request.method=='POST':
        bloodForm=forms.BloodForm(request.POST)
        if bloodForm.is_valid() :        
            bloodgroup=bloodForm.cleaned_data['bloodgroup']
            stock=models.Stock.objects.get(bloodgroup=bloodgroup)
            stock.unit=bloodForm.cleaned_data['unit']
            stock.save()
            messages.success(request,'Successfully Update.')
            user_stocks = dmodels.User_Stock.objects.filter(bloodgroup=bloodgroup)
            for user_stock in user_stocks:
                user_stock.unit = stock.unit
                user_stock.save()

        return HttpResponseRedirect('admin-blood')
    return render(request,'blood/admin_blood.html',context=dict)


@login_required(login_url='adminlogin')
def admin_donor_view(request):
    donors=dmodels.Donor.objects.all()
    return render(request,'blood/admin_donor.html',{'donors':donors})

@login_required(login_url='adminlogin')
def update_donor_view(request,pk):
    donor=dmodels.Donor.objects.get(id=pk)
    user=dmodels.User.objects.get(id=donor.user_id)
    userForm=dforms.DonorUserForm(instance=user)
    donorForm=dforms.DonorForm(request.FILES,instance=donor)
    mydict={'userForm':userForm,'donorForm':donorForm}
    if request.method=='POST':
        userForm=dforms.DonorUserForm(request.POST,instance=user)
        donorForm=dforms.DonorForm(request.POST,request.FILES,instance=donor)
        if userForm.is_valid() and donorForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            donor=donorForm.save(commit=False)
            donor.user=user
            donor.bloodgroup=donorForm.cleaned_data['bloodgroup']
            donor.save()
            messages.success(request,'Successfully Update')
            return redirect('admin-donor')
    return render(request,'blood/update_donor.html',context=mydict)


@login_required(login_url='adminlogin')
def delete_donor_view(request,pk):
    donor=dmodels.Donor.objects.get(id=pk)
    user=User.objects.get(id=donor.user_id)
    user.delete()
    donor.delete()
    messages.success(request,'Successfully deleted user.')
    return HttpResponseRedirect('/admin-donor')

@login_required(login_url='adminlogin')
def admin_patient_view(request):
    patients=pmodels.Patient.objects.all()
    return render(request,'blood/admin_patient.html',{'patients':patients})


@login_required(login_url='adminlogin')
def update_patient_view(request,pk):
    patient=pmodels.Patient.objects.get(id=pk)
    user=pmodels.User.objects.get(id=patient.user_id)
    userForm=pforms.PatientUserForm(instance=user)
    patientForm=pforms.PatientForm(request.FILES,instance=patient)
    mydict={'userForm':userForm,'patientForm':patientForm}
    if request.method=='POST':
        userForm=pforms.PatientUserForm(request.POST,instance=user)
        patientForm=pforms.PatientForm(request.POST,request.FILES,instance=patient)
        if userForm.is_valid() and patientForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            patient=patientForm.save(commit=False)
            patient.user=user
            patient.bloodgroup=patientForm.cleaned_data['bloodgroup']
            patient.save()
            return redirect('admin-patient')
    return render(request,'blood/update_patient.html',context=mydict)

@login_required(login_url='adminlogin')
def delete_patient_view(request,pk):
    patient=pmodels.Patient.objects.get(id=pk)
    user=User.objects.get(id=patient.user_id)
    user.delete()
    patient.delete()
    return HttpResponseRedirect('/admin-patient')

@login_required(login_url='adminlogin')
def admin_request_view(request):
    requests=models.BloodRequest.objects.all().filter(status='Pending')
    return render(request,'blood/admin_request.html',{'requests':requests})

@login_required(login_url='adminlogin')
def admin_request_history_view(request):
    requests=models.BloodRequest.objects.all().exclude(status='Pending')
    return render(request,'blood/admin_request_history.html',{'requests':requests, 'download_url': reverse('download_requests_csv')})

@login_required(login_url='adminlogin')
def download_requests_csv(request):
    requests = models.BloodRequest.objects.exclude(status='Pending')
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="requests.csv"'
    writer = csv.writer(response)
    writer.writerow(['Patient Name', 'Age', 'Reason', 'Blood Group', 'Unit', 'Date', 'Status'])
    for request in requests:
        date_str = request.date.strftime('%Y-%m-%d') if request.date is not None else ''
        writer.writerow([request.patient_name, request.patient_age, request.reason, request.bloodgroup, request.unit, date_str, request.status])
    return response


@login_required(login_url='adminlogin')
def admin_contact_view(request):
    contact=dmodels.Contact.objects.all()
    return render(request,'blood/contact.html',{'contact':contact})
@login_required(login_url='adminlogin')

def delete_contact_view(request,pk):
    contact = dmodels.Contact.objects.get(sno=pk)
    contact.delete()
    messages.success(request,'Successfully Deleted A Message..')

    return HttpResponseRedirect('/admin-contact')





@login_required(login_url='adminlogin')
def admin_donation_view(request):
    donations = dmodels.BloodDonate.objects.all()
    return render(request, 'blood/admin_donation.html', {'donations': donations, 'download_url': reverse('download_donations_csv')})


@login_required(login_url='adminlogin')
def download_donations_csv(request):
    donations = dmodels.BloodDonate.objects.all()
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="donations.csv"'
    writer = csv.writer(response)
    writer.writerow(['Donor', 'Disease', 'Age', 'Weight', 'Sex', 'Blood Group', 'Unit', 'Hemoglobin', 'Date', 'Till','Status',])
    for donation in donations:
        date_str = donation.date.strftime('%Y-%m-%d') if donation.date is not None else ''
        writer.writerow([donation.donor, donation.disease, donation.age, donation.weight, donation.sex, donation.bloodgroup, donation.unit, donation.hemoglobin, donation.date, donation.date_90_days,donation.status])
    return response




@login_required(login_url='adminlogin')
def update_approve_status_view(request,pk):
    req=models.BloodRequest.objects.get(id=pk)
    message=None
    bloodgroup=req.bloodgroup
    unit=req.unit
    stock=models.Stock.objects.get(bloodgroup=bloodgroup)
    if stock.unit > unit:
        stock.unit=stock.unit-unit
        stock.save()
        req.status="Approved"
        messages.success(request,'Successfully Approved.')

        
    else:
        message="Stock Doest Not Have Enough Blood To Approve This Request, Only "+str(stock.unit)+" Unit Available"
    req.save()

    requests=models.BloodRequest.objects.all().filter(status='Pending')
    return render(request,'blood/admin_request.html',{'requests':requests,'message':message})

@login_required(login_url='adminlogin')
def update_reject_status_view(request,pk):
    req=models.BloodRequest.objects.get(id=pk)
    req.status="Rejected"
    req.save()
    messages.error(request,'Successfully Rejected.')

    return HttpResponseRedirect('/admin-request')

@login_required(login_url='adminlogin')
def approve_donation_view(request,pk):
    donation=dmodels.BloodDonate.objects.get(id=pk)
    donation_blood_group=donation.bloodgroup
    donation_blood_unit=donation.unit

    stock=models.Stock.objects.get(bloodgroup=donation_blood_group)
    stock.unit=stock.unit+donation_blood_unit
    stock.save()

    donation.status='Approved'
    donation.save()
    messages.success(request,'Successfully Approved.')

    return HttpResponseRedirect('/admin-donation')


@login_required(login_url='adminlogin')
def reject_donation_view(request,pk):
    donation=dmodels.BloodDonate.objects.get(id=pk)
    donation.status='Rejected'
    donation.save()
    messages.error(request,'Successfully Rejected.')

    return HttpResponseRedirect('/admin-donation')

def donation_events(request):
    return render(request, 'blood/donation_events.html')

def blood_basic(request):
    return render(request, 'blood/blood_basic.html')

def blood_information(request):
    return render(request, 'blood/blood_information.html')

def about_us(request):
    return render(request, 'blood/aboutus.html')

from django.shortcuts import render, redirect
from django.core.mail import send_mail
from .forms import EmailForm

def send_email(request):
    if request.method == 'POST':
        form = EmailForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']
            subject = 'Welcome to Online Blood Bank Management System'

            from_email = settings.EMAIL_HOST_USER            
            send_mail(subject, message, from_email, [email],)
            form.save()
            messages.success(request,'Successfully Replied.')
            print('Correct')

            return redirect('success')
    else:
        form = EmailForm()

    return render(request, 'blood/send_email.html', {'form': form})

def success(request):
    contact=dmodels.Contact.objects.all()
    return render(request,'blood/contact.html',{'contact':contact})


