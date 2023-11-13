from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(CustomUser)
admin.site.register(SickInfoModel)
admin.site.register(HospitalRegistrationModel)
admin.site.register(ContactModel)
admin.site.register(Medicine)
admin.site.register(Patient)
admin.site.register(Department)

admin.site.register(Prescription)
