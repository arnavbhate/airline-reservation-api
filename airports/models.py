from django.db import models

class Airport(models.Model):

    code = models.CharField(max_length=3, primary_key=True)
    name = models.CharField(max_length=60)
    
    def __str__(self):
        return "Airport : " + self.name