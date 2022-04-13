from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import lmsItemSerializer
from .models import lmsItem
import json
#from .models import assignment
# Create your views here.

class lmsItemViews(APIView):
    def get(self, request, lms_id):
        



    def post(self, request):
        serializer = lmsItemSerializer(data = request.data)
        if serializer.is_valid():
           # serializer.save()
            inform = request.data
            dump = json.dumps(inform)
            tmp = json.loads(dump)
            id = tmp['lms_id']
            pw = tmp['lms_pw']
            print(id)
            print(pw)

            return Response("Login Success")
        #({"status" : "success", "data" : serializer.data}, status = status.HTTP_200_OK)
        else:
            return Response("Login Failed")
        #{"status " : "Login Failed", "data" : serializer.errors}, status = status.HTTP_400_BAD_REQUEST)
