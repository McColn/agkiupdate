from django.urls import path
from . import views

urlpatterns = [
    path('', views.home,name='home'),
    path('base/', views.base,name='base'),
    path('registration/', views.registration,name='registration'),
    path('profile/', views.profile,name='profile'),
    path('signin/', views.signin,name='signin'),
    path('signout/', views.signout,name='signout'),
    path('sickinfo/', views.sickinfo,name='sickinfo'),
    path('sickinfolist/', views.sickinfolist,name='sickinfolist'),
    path('sickinfolistprocesed/', views.sickinfolistprocesed,name='sickinfolistprocesed'),
    path('sickinfolistunprocesed/', views.sickinfolistunprocesed,name='sickinfolistunprocesed'),
    path('hospitalRegistration/', views.hospitalRegistration,name='hospitalRegistration'),
    path('registeredHosptal/', views.registeredHosptal,name='registeredHosptal'),
    path('contact_list/', views.contact_list,name='contact_list'),
    path('contactDelete/<int:id>/', views.contactDelete,name='contactDelete'),
    path('patient/', views.patient,name='patient'),
    path('patientList/', views.patientList,name='patientList'),
    path('patientDetail/<int:id>/', views.patientDetail,name='patientDetail'),
    path('patientDelete/<int:id>/', views.patientDelete,name='patientDelete'),
    path('reception/<int:id>/', views.reception,name='reception'),
    path('doctorFirstSession/<int:id>/', views.doctorFirstSession,name='doctorFirstSession'),
    path('doctorSecondSession/<int:id>/', views.doctorSecondSession,name='doctorSecondSession'),
    path('laboratory/<int:id>/', views.laboratory,name='laboratory'),
    path('pharmacy/<int:id>/', views.pharmacy,name='pharmacy'),
    path('userlist/', views.userlist,name='userlist'),
    path('userdelete/<int:id>/', views.userdelete,name='userdelete'),
    path('useredit/<int:id>/', views.useredit,name='useredit'),
    path('sickinfoEdit/<str:pk>/', views.sickinfoEdit,name='sickinfoEdit'),
    path('detailedUser/<int:id>/', views.detailedUser,name='detailedUser'),
    path('hospitalDelete/<int:id>/', views.hospitalDelete,name='hospitalDelete'),
    path('hospitalEdit/<int:id>/', views.hospitalEdit,name='hospitalEdit'),
    path('medicine/', views.medicine,name='medicine'),
    path('medicineAdd/', views.medicineAdd,name='medicineAdd'),
    path('medicineEdit/<int:id>/', views.medicineEdit,name='medicineEdit'),
    path('department/', views.department,name='department'),
    path('departmentAdd/', views.departmentAdd,name='departmentAdd'),
    path('departmentEdit/<int:id>/', views.departmentEdit,name='departmentEdit'),
    path('invoice/<int:id>/', views.invoice,name='invoice'),


    path('prescription_form/', views.prescription_form,name='prescription_form'),
    path('prescription_list/', views.prescription_list,name='prescription_list'),
    path('process_prescription/<int:patient_id>/', views.process_prescription, name='process_prescription'),
    path('edit_prescription/<int:prescription_id>/', views.edit_prescription, name='edit_prescription'),
    path('delete_prescription/<int:prescription_id>/', views.delete_prescription, name='delete_prescription'),
    path('patient_count_per_period/', views.patient_count_per_period, name='patient_count_per_period'),
    path('total_cost_per_period/', views.total_cost_per_period, name='total_cost_per_period'),
    
    

   ]