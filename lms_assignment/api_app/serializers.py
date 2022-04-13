from rest_framework import serializers
from .models import lmsItem

class lmsItemSerializer(serializers.ModelSerializer):
    lms_id = serializers.CharField(max_length = 15)
    lms_pw = serializers.CharField(max_length = 30)

    class Meta:
        model = lmsItem
        fields = ('lms_id', 'lms_pw')
        extra_kwargs = {"lms_pw" : {"write_only" : True}}
