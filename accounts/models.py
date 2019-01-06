from django.db import models

class Announcment(models.Model):
    AnnouncmentID = models.AutoField(primary_key=True)
    text = models.TextField(default="")

    def __str__(self):
        return self.AnnouncmentID