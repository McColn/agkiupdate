from django.forms import ModelForm
from .models import *
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class RegistrationForm(UserCreationForm):
    
    class Meta:
        model = CustomUser
        fields = ['first_name','last_name','age','username','password1','password2','phone']


class UserEditForm(forms.ModelForm):
    department = forms.ModelChoiceField(queryset=Department.objects.all(), empty_label=None)

    
    class Meta:
        model = CustomUser
        fields = ['username','first_name','last_name','age','location','phone','image','department','is_doctor','is_laboratorist','is_receptionist','is_patient','is_pharmacist']


class SickInfoForm(forms.ModelForm):
    
    class Meta:
        model = SickInfoModel
        fields = ['mtaa','kata','wilaya','maelezo','hospital']


class SickInfoEditForm(forms.ModelForm):
    
    class Meta:
        model = SickInfoModel
        fields = ['hospital']


class HospitalRegistrationForm(forms.ModelForm):
    
    class Meta:
        model = HospitalRegistrationModel
        fields = ['name','level','location']

class HospitalEditForm(forms.ModelForm):
    
    class Meta:
        model = HospitalRegistrationModel
        fields = ['name','level','location']


class ContactForm(forms.ModelForm):
    
    class Meta:
        model = ContactModel
        fields = ['jina','phone','ujumbe']


class PatientSearchForm(forms.ModelForm):

    class Meta:
        model = Patient
        fields = ['fullname']

class PatientForm(forms.ModelForm):

    class Meta:
        model = Patient
        fields = ['fullname','age','address','gender','height','pressure','weight']


class ReceptionForm(forms.ModelForm):

    class Meta:
        model = Patient
        fields = ['fullname','age','address','gender','height','pressure','weight']   


class DoctorFirstSessionForm(forms.ModelForm):

    class Meta:
        model = Patient
        fields = ['dalili','possibleDiseases']   


class LaboratoryForm(forms.ModelForm):

    class Meta:
        model = Patient
        fields = ['labResults','testConducted']  


class DoctorSecondSessionForm(forms.ModelForm):

    class Meta:
        model = Patient
        fields = ['actualDiseases','otherRecomendation']  

    


class PharmacyForm(forms.ModelForm):

    class Meta:
        model = Prescription
        fields = ['cost']  


class MedicineAddForm(forms.ModelForm):

    class Meta:
        model = Medicine
        fields = ['medicineName','amount','unitCost','expireDate']  

class MedicineEditForm(forms.ModelForm):

    class Meta:
        model = Medicine
        fields = ['medicineName','amount','unitCost','expireDate']  


class DepartmentForm(forms.ModelForm):

    class Meta:
        model = Department
        fields = ['name','descrption']   



# prescriptions/forms.py



class PrescriptionForm(forms.Form):
    # patient = forms.ModelChoiceField(queryset=Patient.objects.all(), label='Patient')
    medicines = forms.ModelMultipleChoiceField(queryset=Medicine.objects.all(), widget=forms.CheckboxSelectMultiple, label='Medicine')
    
    # dosage = forms.CharField(max_length=100, label='Dosage')
    # amount = forms.IntegerField(min_value=1, label='Amount')
    # cost = forms.IntegerField(min_value=1, label='Cost')
    # prescription_date = forms.DateField(label='prescription_date')
