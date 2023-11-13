from django.shortcuts import render, redirect,get_object_or_404
from .models import *
from app.forms import *
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from datetime import date
from django.urls import reverse
from django.db.models import Sum
from datetime import datetime, timedelta
from django.utils import timezone


# Create your views here.
def home(request):

    today = date.today()
    today_total_patients = Patient.objects.filter(date__date=today).count()
    overall_total_patients = Patient.objects.all().count()

    registered = CustomUser.objects.all()
    registered_total = registered.count()

    newsick = SickInfoModel.objects.exclude(hospital__isnull=False)
    newsick_total = newsick.count()

    hospitals = HospitalRegistrationModel.objects.all()
    hospital_total = hospitals.count()

    jumbe = ContactModel.objects.all()
    jumbe_total = jumbe.count()

    # Get total cost per day
    day_total_cost = Prescription.objects.filter(prescription_date=timezone.now().date()).aggregate(Sum('totalCost'))['totalCost__sum']

    # Get total cost per week
    current_week_number = timezone.now().isocalendar()[1]
    week_total_cost = Prescription.objects.filter(prescription_date__week=current_week_number).aggregate(Sum('totalCost'))['totalCost__sum']

    # Get total cost per month
    current_month = timezone.now().month
    month_total_cost = Prescription.objects.filter(prescription_date__month=current_month).aggregate(Sum('totalCost'))['totalCost__sum']

    # Get total cost per year
    current_year = timezone.now().year
    year_total_cost = Prescription.objects.filter(prescription_date__year=current_year).aggregate(Sum('totalCost'))['totalCost__sum']

    
    x = CustomUser.objects.exclude(is_patient=True)
    form = ContactForm()
    if request.method=='POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"message submitted successfully")
            return redirect('home')
        
    context = {
        'registered':registered,
        'registered_total':registered_total,
        'newsick':newsick,
        'newsick_total':newsick_total,
        'hospitals':hospitals,
        'hospital_total':hospital_total,
        'jumbe':jumbe,
        'jumbe_total':jumbe_total,
        'today_total_patients': today_total_patients,
        'overall_total_patients': overall_total_patients,
        'form':form,
        'x':x,
        'day_total_cost': day_total_cost,
        'week_total_cost': week_total_cost,
        'month_total_cost': month_total_cost,
        'year_total_cost': year_total_cost,
    }
    return render(request,'app/home.html',context)

def base(request):
    return render(request,'app/base.html')



def registration(request):
    form = RegistrationForm()
    if request.method=='POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('signin')
        else:
            messages.error(request,'Bad authenticate')
			

    context = {
            'form':form
        }

    return render(request,'app/registration.html',context)

def userlist(request):
    x = CustomUser.objects.all().order_by('-id')
    context = {
        'x':x
    }
    return render(request,'app/userlist.html',context)

def useredit(request, id):
    s = CustomUser.objects.get(id=id)
    departments = Department.objects.all()

    if request.method == 'POST':
        form = UserEditForm(request.POST, request.FILES, instance=s)  # Include request.FILES
        if form.is_valid():
            form.save()
            return redirect('userlist')
    else:
        form = UserEditForm(instance=s)
    context = {
        'form': form,
        's': s,
        'departments':departments,
    }
    return render(request, 'app/useredit.html', context)


def userdelete(request,id):
    x = get_object_or_404(CustomUser,id=id)
    x.delete()
    return redirect('userlist')

def profile(request):
    return render(request, 'app/profile.html')

def signin(request):

    if request.method == 'POST':
        username = request.POST['username']
        password1 = request.POST['password1']
        user = authenticate(username=username,password=password1)

        if user is not None:
            login(request,user)
            return render(request,'app/home.html')
        else:
            messages.error(request,'Bad authenticate')
            return redirect('signin')
    return render(request,'app/signin.html')


def signout(request):
    logout(request)
    return redirect ('home')
    return render(request,'app/signout.html')

@login_required
def sickinfo(request):
    # form = SickInfoForm()
    if request.method=='POST':
        form = SickInfoForm(request.POST)
        if form.is_valid():
            report = form.save(commit=False)
            report.user=request.user
            report.save()
            return redirect('home')
    else:
        form = SickInfoForm()

    context = {
            'form':form
         }

    return render(request,'app/sickinfo.html',context)

def sickinfoEdit(request,pk):
    s = SickInfoModel.objects.get(pk=pk)
    form = SickInfoEditForm(instance=s)
    if request.method=='POST':
        form = SickInfoEditForm(request.POST,instance=s)
        if form.is_valid():
            form.save()
            
            return redirect('sickinfolist')
    context = {
            'form':form,
            's':s
         }

    return render(request,'app/sickinfoEdit.html',context)

def sickinfolist(request):
    x = SickInfoModel.objects.all().order_by('-id')
    context = {
        'x':x
    }
    return render(request,'app/sickinfolist.html',context)

def sickinfolistprocesed(request):
    x = SickInfoModel.objects.exclude(hospital__isnull=True)
    context = {
        'x':x
    }
    return render(request,'app/sickinfolistprocesed.html',context)


def sickinfolistunprocesed(request):
    x = SickInfoModel.objects.exclude(hospital__isnull=False)
    context = {
        'x':x
    }
    return render(request,'app/sickinfolistunprocesed.html',context)
def hospitalRegistration(request):
    form = HospitalRegistrationForm()
    if request.method=='POST':
        form = HospitalRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"you added hospital successfully")
            return redirect('hospitalRegistration')
    context = {
            'form':form
        }
    return render(request,'app/hospitalRegistration.html',context)


def registeredHosptal(request):
    x = HospitalRegistrationModel.objects.all().order_by('-id')
    
    context = {
            'x':x
        }
    return render(request,'app/registeredHosptal.html',context)

def hospitalDelete(request,id):
    x = get_object_or_404(HospitalRegistrationModel,id=id)
    x.delete()
    return redirect('registeredHosptal')

def hospitalEdit(request,id):
    s = HospitalRegistrationModel.objects.get(id=id)
    form = HospitalEditForm(instance=s)
    if request.method=='POST':
        form = HospitalEditForm(request.POST,instance=s)
        if form.is_valid():
            form.save()
            
            return redirect('registeredHosptal')
    context = {
            'form':form,
            's':s
         }

    return render(request,'app/hospitalEdit.html',context)




def contact_list(request):
    x = ContactModel.objects.all()
    
    context = {
            'x':x
        }
    
    return render(request,'app/contact_list.html',context)

def contactDelete(request,id):
    x = get_object_or_404(ContactModel,id=id)
    x.delete()
    return redirect('contact_list')


def detailedUser(request,id):
    detaileduser = CustomUser.objects.get(id=id)
    context = {
        'detaileduser':detaileduser
    }
    return render(request,'app/detailedUser.html',context)
    

def patient(request):
    form = PatientForm()
    if request.method=='POST':
        form = PatientForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"patient added successfully")
            return redirect('patientList')
    context = {
            'form':form
        }
    return render(request,'app/patient.html',context)
    

def patientList(request):
    form = PatientSearchForm(request.POST or None)
    x = Patient.objects.all().order_by('-id')
    patients = Patient.objects.all()

    if request.method == 'POST':
        patients = Patient.objects.filter(fullname__icontains=form['fullname'].value())
    context = {
            'x':x,
            'form':form,
            'patients':patients
            
        }
    return render(request,'app/patientList.html',context)

def patientDetail(request,id):
    x = Patient.objects.get(id=id)
    prescriptions = Prescription.objects.filter(patient=x)

    # Calculate the total cost for the patient
    sum_total_cost = sum([prescription.totalCost for prescription in prescriptions])


    context = {
        'x':x,
        'prescriptions':prescriptions,
        'sum_total_cost':sum_total_cost,
    }
    return render(request,'app/patientDetail.html',context)

def patientDelete(request,id):
    x = get_object_or_404(Patient,id=id)
    x.delete()
    return redirect('patientList')


def reception(request,id):
    s = Patient.objects.get(id=id)
    form = ReceptionForm(instance=s)
    if request.method=='POST':
        form = ReceptionForm(request.POST,instance=s)
        if form.is_valid():
            form.save()
            
            return redirect(reverse('patientDetail', args=[id]))
    context = {
            'form':form,
            's':s
         }

    return render(request,'app/reception.html',context)


def doctorFirstSession(request,id):
    s = Patient.objects.get(id=id)
    form = DoctorFirstSessionForm(instance=s)
    if request.method=='POST':
        form = DoctorFirstSessionForm(request.POST,instance=s)
        if form.is_valid():
            form.save()
            
            return redirect(reverse('patientDetail', args=[id]))
    context = {
            'form':form,
            's':s
         }

    return render(request,'app/doctorFirstSession.html',context)


def laboratory(request,id):
    s = Patient.objects.get(id=id)
    form = LaboratoryForm(instance=s)
    if request.method=='POST':
        form = LaboratoryForm(request.POST,instance=s)
        if form.is_valid():
            form.save()
            
            return redirect(reverse('patientDetail', args=[id]))
    context = {
            'form':form,
            's':s
         }

    return render(request,'app/laboratory.html',context)


def doctorSecondSession(request,id):
    s = Patient.objects.get(id=id)
    form = DoctorSecondSessionForm(instance=s)
    
    if request.method=='POST':
        form = DoctorSecondSessionForm(request.POST,instance=s)
        if form.is_valid():
            form.save()
            
            return redirect(reverse('patientDetail', args=[id]))
    context = {
            'form':form,
            's':s,
            
         }

    return render(request,'app/doctorSecondSession.html',context)


def pharmacy(request,id):
    s = Patient.objects.get(id=id)
    form = PharmacyForm(instance=s)
    if request.method=='POST':
        form = PharmacyForm(request.POST,instance=s)
        if form.is_valid():
            form.save()
            
            return redirect(reverse('patientDetail', args=[id]))
    context = {
            'form':form,
            's':s
         }

    return render(request,'app/pharmacy.html',context)


def medicine(request):
    medicines = Medicine.objects.all()
    return render(request, 'app/medicine.html', {'medicines': medicines})


def medicineAdd(request):
    form = MedicineAddForm()
    if request.method=='POST':
        form = MedicineAddForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"medicine added successfully")
            return redirect('medicineAdd')
    context = {
            'form':form
        }
    return render(request,'app/medicineAdd.html',context)

def medicineEdit(request,id):
    s = Medicine.objects.get(id=id)
    form = MedicineEditForm(instance=s)
    if request.method=='POST':
        form = MedicineEditForm(request.POST,instance=s)
        if form.is_valid():
            form.save()
            
            return redirect('medicine')
    context = {
            'form':form,
            's':s
         }

    return render(request,'app/medicineEdit.html',context)


def invoice(request,id):
    x = Patient.objects.get(id=id)
    prescriptions = Prescription.objects.filter(patient=x)
    # Calculate the total cost for the patient
    sum_total_cost = sum([prescription.totalCost for prescription in prescriptions])


    context = {
        'x':x,
        'prescriptions':prescriptions,
        'sum_total_cost':sum_total_cost,
    }
    return render(request,'app/invoice.html',context)


def department(request):
    x = Department.objects.all()
    context = {
        'x':x,
    }
    return render(request,'app/department.html',context)

def departmentAdd(request):
    form = DepartmentForm()
    if request.method=='POST':
        form = DepartmentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"department added successfully")
            return redirect('department')
    context = {
            'form':form,
        }
    return render(request,'app/departmentAdd.html',context)

def departmentEdit(request,id):
    s = Department.objects.get(id=id)
    form = DepartmentForm(instance=s)
    if request.method=='POST':
        form = DepartmentForm(request.POST,instance=s)
        if form.is_valid():
            form.save()
            
            return redirect('department')
    context = {
            'form':form,
            's':s
         }

    return render(request,'app/departmentEdit.html',context)






# prescriptions/views.py



def prescription_form(request):
    if request.method == 'POST':
        form = PrescriptionForm(request.POST)
        if form.is_valid():
            patient = form.cleaned_data['patient']
            medicines = form.cleaned_data['medicines']
            dosage = form.cleaned_data['dosage']
            amount = form.cleaned_data['amount']
            prescription_date = form.cleaned_data['prescription_date']

            for medicine in medicines:
                # Save prescription data to the database for each selected medicine
                prescription = Prescription.objects.create(
                    medicine=medicine,
                    patient=patient,
                    dosage=dosage,
                    amount=amount,
                    prescription_date=prescription_date,
                )
                prescription.save()

            # Redirect to a success page or display a success message
            # return HttpResponseRedirect('/success/')
    else:
        form = PrescriptionForm()

    return render(request, 'app/prescription_form.html', {'form': form})


# prescriptions/views.py



def prescription_list(request):
    prescriptions = Prescription.objects.select_related('medicine', 'patient').order_by('patient__fullname')

    grouped_prescriptions = {}
    for prescription in prescriptions:
        patient_name = prescription.patient.fullname
        if patient_name not in grouped_prescriptions:
            grouped_prescriptions[patient_name] = []
        grouped_prescriptions[patient_name].append({
            'medicine': prescription.medicine.medicineName,
            'dosage': prescription.dosage,
            'amount': prescription.amount
        })

    return render(request, 'app/prescription_list.html', {'prescriptions': grouped_prescriptions})


# # update


def edit_prescription(request, prescription_id):
    prescription = get_object_or_404(Prescription, id=prescription_id)
    prescription = Prescription.objects.get(patient_id=x.id)

    if request.method == 'POST':
        form = PrescriptionForm(request.POST, instance=prescription)
        if form.is_valid():
            form.save()
            # Redirect to a success page or display a success message
            return redirect('patientDetail', id=prescription.patient.id)
    else:
        form = PrescriptionForm(instance=prescription)

    context = {
        'form': form,
        'prescription': prescription,
    }
    return render(request, 'app/edit_prescription.html', context)




def process_prescription(request, patient_id):
    patient = Patient.objects.get(id=patient_id)

    if request.method == 'POST':
        form = PrescriptionForm(request.POST)
        if form.is_valid():
            selected_medicines = form.cleaned_data['medicines']
            # Process selected medicines, create PrescriptionDetail objects here
            for medicine in selected_medicines:
                dosage = request.POST.get(f'dosage_{medicine.id}')  # Assuming you have inputs with names like 'dosage_1', 'dosage_2', etc.
                cost = request.POST.get(f'cost_{medicine.id}')  # Similarly, inputs for cost
                amount = request.POST.get(f'amount_{medicine.id}')  # Similarly, inputs for cost
                totalCost = request.POST.get(f'totalCost_{medicine.id}')  # Similarly, inputs for cost

                # Create PrescriptionDetail objects with selected medicine, dosage, and cost
                Prescription.objects.create(medicine=medicine, patient=patient, dosage=dosage, cost=cost,amount=amount,totalCost=totalCost)

                # Decrease remainAmount of associated Medicine
                # if amount is not None and medicine.remainAmount >= int(amount):
                #     medicine.remainAmount -= int(amount)
                #     medicine.save()

            # Redirect or show success message
            # return HttpResponseRedirect('/success/')
    else:
        form = PrescriptionForm()

    return render(request, 'app/process_prescription.html', {'form': form, 'patient': patient})



def delete_prescription(request, prescription_id):
    prescription = get_object_or_404(Prescription, id=prescription_id)

    if request.method == 'POST':
        # Get the prescription details before deletion
        medicine = prescription.medicine
        patient = prescription.patient
        amount_given = prescription.amount

        # Restore the remainAmount of the medicine
        if medicine:
            medicine.remainAmount += amount_given
            medicine.save()

        # Delete the prescription
        prescription.delete()
        messages.success(request, 'Prescription deleted successfully.')

        # Redirect to the patientDetail page with the appropriate patient id
        return redirect('patientDetail', id=patient.id)

    # Redirect to the patientDetail page with a default patient id if not a POST request
    
    return redirect('patientDetail', id=prescription.patient.id)



def patient_count_per_period(request):
    # Get the current day of the week
    current_day = datetime.now().strftime('%A')
    current_month = datetime.now().month
    current_year = datetime.now().year
    current_year = datetime.now().year


    # Assuming your Patient model has a field named 'date'
    # Replace 'date' with the actual field name in your model
    patients_per_day = Patient.objects.values('date').annotate(patient_count=models.Count('id'))
    patients_per_month = Patient.objects.filter(date__month=current_month, date__year=current_year)
    patients_per_year = Patient.objects.filter(date__year=current_year)


    # Make current_date offset-aware
    current_date = timezone.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)

    # Prepare data for each week of the month
    weeks_data = []
    months_data = []

    # Calculate the start and end dates for each week
    while current_date.month == current_month:
        week_start = current_date
        week_end = current_date + timedelta(days=6, hours=23, minutes=59, seconds=59)
        week_data = {
            'week_start': week_start,
            'week_end': week_end,
            'patient_count': patients_per_month.filter(date__range=(week_start, week_end)).count()
        }
        weeks_data.append(week_data)
        current_date = week_end + timedelta(days=1)


    # Prepare data for each day of the week (Monday to Sunday)
    days_data = [
        {'day_name': 'Monday', 'patient_count': 0},
        {'day_name': 'Tuesday', 'patient_count': 0},
        {'day_name': 'Wednesday', 'patient_count': 0},
        {'day_name': 'Thursday', 'patient_count': 0},
        {'day_name': 'Friday', 'patient_count': 0},
        {'day_name': 'Saturday', 'patient_count': 0},
        {'day_name': 'Sunday', 'patient_count': 0}
    ]


    # Calculate the start and end dates for each month
    for month in range(1, 13):
        month_start = timezone.now().replace(year=current_year, month=month, day=1, hour=0, minute=0, second=0, microsecond=0)
        month_end = month_start + timedelta(days=31)  # Assuming the maximum number of days in a month
        month_data = {
            'month_name': month_start.strftime('%B'),  # Get the month name
            'patient_count': patients_per_year.filter(date__range=(month_start, month_end)).count()
        }
        months_data.append(month_data)


    # Update data with actual patient counts
    for day_data in days_data:
        day_number = {'Monday': 0, 'Tuesday': 1, 'Wednesday': 2, 'Thursday': 3, 'Friday': 4, 'Saturday': 5, 'Sunday': 6}[day_data['day_name']]
        day_data['patient_count'] = sum(1 for item in patients_per_day if item['date'].weekday() == day_number)

    # for week_data in weeks_data:
    #     week_data['patient_count'] = sum(1 for item in patients_per_month if week_data['week_start'] <= item['date'] <= week_data['week_end'])

    context = {
        'days_data': days_data, 
        'current_day': current_day,
        'weeks_data': weeks_data, 'current_month': current_month, 'current_year': current_year,
        'months_data': months_data, 'current_year': current_year,
        }
    
    
    return render(request, 'app/patient_count_per_period.html', context)




def total_cost_per_period(request):
    # Assuming Prescription model has a 'prescription_date' field
    prescriptions = Prescription.objects.all()

    # Calculate the start and end dates for each week of the month
    current_date = timezone.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    weeks_data = []

    while current_date.month == timezone.now().month:
        week_start = current_date
        week_end = current_date + timedelta(days=6, hours=23, minutes=59, seconds=59)

        # Aggregate total cost for prescriptions within the week
        total_cost = prescriptions.filter(prescription_date__range=(week_start, week_end)).aggregate(Sum('totalCost'))['totalCost__sum'] or 0

        week_data = {
            'week_start': week_start,
            'week_end': week_end,
            'total_cost': total_cost
        }

        weeks_data.append(week_data)
        current_date = week_end + timedelta(days=1)

    
     # Get the current date
    current_date = timezone.now().date()

    # Calculate the start and end dates of the current week (Monday to Sunday)
    start_of_week = current_date - timedelta(days=current_date.weekday())
    end_of_week = start_of_week + timedelta(days=6)

    # Query the Prescription model for entries within the current week
    prescriptions_in_week = Prescription.objects.filter(
        prescription_date__range=[start_of_week, end_of_week]
    )

    # Prepare data for each day of the week (Monday to Sunday)
    days_data = [
        {'day_name': 'Sunday', 'total_cost': 0},
        {'day_name': 'Monday', 'total_cost': 0},
        {'day_name': 'Tuesday', 'total_cost': 0},
        {'day_name': 'Wednesday', 'total_cost': 0},
        {'day_name': 'Thursday', 'total_cost': 0},
        {'day_name': 'Friday', 'total_cost': 0},
        {'day_name': 'Saturday', 'total_cost': 0},
        
    ]

    # Calculate the total cost for each day of the week
    for day_entry in days_data:
        day_name = day_entry['day_name']
        total_cost_for_day = prescriptions_in_week.filter(prescription_date__week_day=days_data.index(day_entry) + 1).aggregate(Sum('totalCost'))['totalCost__sum']

        # If there are no prescriptions for a particular day, set the total cost to 0
        day_entry['total_cost'] = total_cost_for_day if total_cost_for_day is not None else 0



    # Calculate the start and end dates of the current year (January 1st to December 31st)
    start_of_year = current_date.replace(month=1, day=1)
    end_of_year = current_date.replace(month=12, day=31)

    # Query the Prescription model for entries within the current year
    prescriptions_in_year = Prescription.objects.filter(
        prescription_date__range=[start_of_year, end_of_year]
    )

    # Prepare data for each month of the year (January to December)
    months_data = [
        {'month_name': 'January', 'total_cost': 0},
        {'month_name': 'February', 'total_cost': 0},
        {'month_name': 'March', 'total_cost': 0},
        {'month_name': 'April', 'total_cost': 0},
        {'month_name': 'May', 'total_cost': 0},
        {'month_name': 'June', 'total_cost': 0},
        {'month_name': 'July', 'total_cost': 0},
        {'month_name': 'August', 'total_cost': 0},
        {'month_name': 'September', 'total_cost': 0},
        {'month_name': 'October', 'total_cost': 0},
        {'month_name': 'November', 'total_cost': 0},
        {'month_name': 'December', 'total_cost': 0},
    ]

    # Calculate the total cost for each month of the year
    for month_entry in months_data:
        month_name = month_entry['month_name']
        total_cost_for_month = prescriptions_in_year.filter(prescription_date__month=months_data.index(month_entry) + 1).aggregate(Sum('totalCost'))['totalCost__sum']

        # If there are no prescriptions for a particular month, set the total cost to 0
        month_entry['total_cost'] = total_cost_for_month if total_cost_for_month is not None else 0


    context = {
        'weeks_data': weeks_data,'days_data':days_data,'months_data':months_data,
    }

    return render(request, 'app/total_cost_per_period.html', context)
    
