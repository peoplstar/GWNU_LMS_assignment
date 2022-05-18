from django.db import models

# Create your models here.
class lmsItem(models.Model):
    lms_id = models.CharField(max_length = 15, primary_key = True)
    lms_pw = models.CharField(max_length = 150)
    firebaseToken = models.CharField(max_length = 200)

