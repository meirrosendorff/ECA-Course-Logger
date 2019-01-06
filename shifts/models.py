from django.db import models


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