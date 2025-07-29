
from django.db import models

class PillReminder(models.Model):
    name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)
    medicine = models.CharField(max_length=100)
    time = models.DateTimeField()

    def __str__(self):
        return f"{self.name} - {self.medicine} at {self.time}"
