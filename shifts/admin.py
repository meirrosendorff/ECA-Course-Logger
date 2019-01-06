from django.contrib import admin

from .models import *


admin.site.register(ServiceType)
admin.site.register(Service)
admin.site.register(Shift)
admin.site.register(ShiftType)
admin.site.register(studentShift)