from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User
from django.db.models.base import Model
from django.contrib.auth import get_user_model
import random
import string


# Create your models here.

class Department(models.Model):
    name = models.CharField(max_length=20)
    descrption = models.CharField(max_length=20)


class CustomUser(AbstractUser):
    phone = models.CharField(max_length=15, null=True,blank=True)
    location = models.CharField(max_length=30, null=True, blank=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, null=True,blank=True)
    reg_no = models.CharField(max_length=10, unique=True)
    age = models.IntegerField(null=True)
    image = models.ImageField(upload_to ='media/',blank=True,null=True)
    is_doctor = models.BooleanField(default=False)
    is_laboratorist = models.BooleanField(default=False)
    is_receptionist = models.BooleanField(default=False)
    is_pharmacist = models.BooleanField(default=False)
    is_patient = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        if not self.reg_no:
            # Generate unique registration number using initials and random string
            initials = ''.join(word[0] for word in self.first_name.split()) + ''.join(word[0] for word in self.last_name.split())
            random_string = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
            self.reg_no = initials.upper() + random_string

        super().save(*args, **kwargs)

    def __str__(self):
        return self.username



class HospitalRegistrationModel(models.Model):
    name = models.CharField(max_length=20)
    level = models.CharField(max_length=20)
    location = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class SickInfoModel(models.Model):
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    mtaa = models.CharField(max_length=15)
    kata = models.CharField(max_length=30)
    wilaya = models.CharField(max_length=30)
    maelezo = models.TextField(max_length=1000)
    mda = models.DateTimeField(auto_now_add=True)
    hospital = models.ForeignKey(HospitalRegistrationModel, on_delete=models.CASCADE,null=True,blank=True)
    hospital_assigned = models.BooleanField(default=False)
    

    def __str__(self):
        return self.user.username



class ContactModel(models.Model):
    jina = models.CharField(max_length=20)
    phone = models.CharField(max_length=20)
    ujumbe = models.CharField(max_length=200)

    def __str__(self):
        return self.jina


class Medicine(models.Model):
    medicineName = models.CharField(max_length=20)
    amount = models.IntegerField()
    remainAmount = models.IntegerField()
    unitCost = models.FloatField()
    
    receivedDate = models.DateTimeField(auto_now_add=True)
    expireDate= models.DateField()

    @property
    def totalCost(self):
        # Calculate and return total cost dynamically
        return round(self.amount * self.unitCost, 2)
    
    def save(self, *args, **kwargs):
        # Set a default value for remainAmount if not provided
        if self.remainAmount is None:
            self.remainAmount = self.amount

        super().save(*args, **kwargs)
    
    

    def __str__(self):
        return self.medicineName


class Patient(models.Model):
    fullname = models.CharField(max_length=30)
    age = models.IntegerField()
    address = models.CharField(max_length=30)
    gender = models.CharField(max_length=10)
    height = models.IntegerField(null=True,blank=True)
    pressure = models.CharField(max_length=10,null=True,blank=True)
    weight = models.IntegerField(null=True,blank=True)
    date = models.DateTimeField(auto_now_add=True)
    dalili = models.TextField(max_length=500,null=True,blank=True)
    possibleDiseases = models.TextField(max_length=500,null=True,blank=True)
    testConducted = models.TextField(max_length=500,null=True,blank=True)
    labResults = models.TextField(max_length=500,null=True,blank=True)
    actualDiseases = models.TextField(max_length=500,null=True,blank=True)
    otherRecomendation = models.TextField(max_length=500,null=True,blank=True)
    
    def __str__(self):
        return self.fullname



# prescriptions/models.py

class Prescription(models.Model):
    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    amount = models.PositiveIntegerField(null=True,blank=True)
    dosage = models.CharField(max_length=100,null=True,blank=True)
    cost = models.FloatField(null=True,blank=True)
    totalCost = models.FloatField(null=True, blank=True) 
    medicineStatus = models.BooleanField(default=False)
    prescription_date = models.DateField(auto_now_add=True)
    id = models.AutoField(primary_key=True)

    @property
    def day_of_week(self):
        # Assuming prescription_date is an attribute of type datetime.datetime
        return self.prescription_date.strftime('%A')

    def __str__(self):
        return f"Prescription for {self.medicine.medicineName} to {self.patient.fullname}"

    def save(self, *args, **kwargs):
        # Set the cost to the unitCost of the selected medicine
        self.cost = self.medicine.unitCost if self.medicine else None

        # Ensure that self.amount is a numeric value before attempting multiplication
        try:
            if self.amount:
                self.amount = int(self.amount)  # Try converting to integer
        except (ValueError, TypeError):
            self.amount = None

        # Calculate the total cost based on cost and amount
        self.totalCost = round(self.cost * self.amount, 2) if self.cost and self.amount else None

        # Decrease remainAmount of associated Medicine
        if self.amount and self.medicine.remainAmount >= self.amount:
            self.medicine.remainAmount -= self.amount
            self.medicine.save()
            
        super().save(*args, **kwargs)
