from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator
from datetime import datetime, timedelta
from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import date, timedelta
from django.contrib.auth.models import User




class Donor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_pic= models.ImageField(upload_to='profile_pic/Donor/',null=True,blank=True)
    bloodgroup=models.CharField(max_length=10)
    email = models.EmailField(unique=True)
    otp = models.CharField(max_length=25,default='0000')
    address = models.CharField(max_length=40)
    mobile = models.CharField(max_length=10,null=False)
    last_donation = models.DateTimeField(null=True, blank=True)

    @property
    def get_name(self):
        return self.user.first_name+" "+self.user.last_name
    @property
    def get_instance(self):
        return self
    def __str__(self):
        return self.user.first_name
def default_date_90_days():
    return date.today() + timedelta(days=90)

class BloodDonate(models.Model): 
    donor=models.ForeignKey(Donor,on_delete=models.CASCADE)   
    disease=models.CharField(max_length=100,default="Nothing")
    age = models.PositiveIntegerField(validators=[MinValueValidator(18), MaxValueValidator(65)])
    weight = models.DecimalField(max_digits=5, decimal_places=2, default=0 ,validators=[MinValueValidator(45)])
    SEX_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )
    sex = models.CharField(max_length=1, choices=SEX_CHOICES, default='M')
    bloodgroup=models.CharField(max_length=10,)
    unit=models.PositiveIntegerField(default=0)
    hemoglobin = models.PositiveIntegerField(default=0, validators=[MinValueValidator(12.5)])
    status=models.CharField(max_length=20,default="Pending")
    date=models.DateField(auto_now=True)
    date_90_days = models.DateField(default=default_date_90_days)

    def __str__(self):
        return f"{self.donor} - ({self.date})"
    
class User_Stock(models.Model):
    bloodgroup=models.CharField(max_length=10)
    unit=models.PositiveIntegerField(default=0)
    def __str__(self):
        return self.bloodgroup
    



class Contact(models.Model):
     sno= models.AutoField(primary_key=True)
     name= models.CharField(max_length=255)
     phone= models.CharField(max_length=13)
     email= models.CharField(max_length=100)
     content= models.TextField()
     timeStamp=models.DateTimeField(auto_now_add=True, blank=True)

     def __str__(self):
          return "Message from " + self.name + ' - ' + self.email
