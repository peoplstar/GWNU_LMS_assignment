from django.db import models

# Create your models here.
class lmsItem(models.Model):
    lms_id = models.CharField(max_length = 15, primary_key = True)
    lms_pw = models.CharField(max_length = 30)
    # FirebaseToken = models.CharField(max_length = )
"""
class assignment(models.Model):
    course = models.CharField(max_length = 20)
    title = models.CharField(max_length = 100, primary_key = True)
    d_day_start = models.DateTimeField(input_formats=['%Y-%m-%d %H:%M'])
    d_day_end = models.DateTimeField(input_formats=['%Y-&m-%d %H:%M'])
    clear = models.CharField(max_length = 10)
    content = models.CharField(max_length = 200)
"""

