from django.db import models
from django.conf import settings

class ServiceType(models.Model):
    serviceTypeID = models.AutoField(primary_key=True)
    name = models.CharField(max_length=500, null=False, unique=True)

    def __str__(self):
        return self.name

class Service(models.Model):
    serviceID = models.AutoField(primary_key=True)
    name = models.CharField(max_length=500, null=False, unique=True)
    serviceType = models.ForeignKey(ServiceType, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class ShiftType(models.Model):
    shiftTyepID = models.AutoField(primary_key=True)
    name = models.CharField(max_length=500, null=False, unique=True)


    def save(self, *args, **kwargs):
        self.full_clean()  # performs regular validation then clean()
        super(ShiftType, self).save(*args, **kwargs)

    def clean(self):
        if self.name:
            self.name = self.name.replace(" ", "_")

    def __str__(self):
        return self.name

class Shift(models.Model):
    shiftID = models.AutoField(primary_key=True)
    shiftType = models.ForeignKey(ShiftType, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    startDate = models.DateField(null=False)
    startTime = models.TimeField(null=False)
    hours = models.IntegerField(default=0)
    placesAvailable = models.IntegerField(default=0)
    placesFilled = models.IntegerField(default=0)

    def __str__(self):
        return self.service.name + " - " + str(self.startDate) + " at " + str(self.startTime)

class studentShift(models.Model):
    shift = models.ForeignKey(Shift, on_delete=models.CASCADE)
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
