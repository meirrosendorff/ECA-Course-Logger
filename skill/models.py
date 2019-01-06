from django.db import models
from shifts.models import Service
from django.conf import settings

class SkillCategory(models.Model):
    categoryID = models.AutoField(primary_key=True)
    name = models.CharField(max_length=500, null=False, unique=True)

    def __str__(self):
        return self.name


class Skill(models.Model):

    skillID = models.AutoField(primary_key=True)
    skillCategory = models.ForeignKey(SkillCategory, on_delete=models.CASCADE)
    name = models.CharField(max_length=500, null=False, unique=True)
    attemptsRequired = models.IntegerField(default=0)

    def __str__(self):
        return self.name


class SkillPerformed(models.Model):

    skillPerformedID = models.AutoField(primary_key=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    supervisor = models.CharField(max_length=100, null=False)
    date = models.DateField(null=False)
    time = models.TimeField(null=False)
    comment = models.TextField(null=True)

    def __str__(self):
        return self.user.username + " - " + self.skill.name