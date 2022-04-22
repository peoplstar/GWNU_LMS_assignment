from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import lmsItemSerializer
from .models import lmsItem
from selenium.common.exceptions import UnexpectedAlertPresentException as PE # 로그인 오류

import Pldd
import json
import firebaseLink
# from .models import assignment
# Create your views here.

class lmsItemViews(APIView):
    '''
    def get(self, request, lms_id):
        return(RSA 공개키를 전달)
    '''



    def post(self, request):
        serializer = lmsItemSerializer(data = request.data)
        if serializer.is_valid():
            # serializer.save()
            inform = request.data
            dump = json.dumps(inform)
            tmp = json.loads(dump)
            userid = tmp['lms_id']
            password = tmp['lms_pw']
            
            # Crawling Method Parameter 
            crawSystem = Pldd.crawling(userid, password)
            
            try :
                txt = crawSystem.craw()
                status_code = 200
            except PE :
                txt = 'Login Failed'
                status_code = 400
                
            
            # JSON DB data processing
            firedb = firebaseLink.DBLink(userid)
            firedb.rwJson("")
            firedb.Link("")
            
            if status_code == 200:
                return Response(txt, status = status.HTTP_200_OK)
            else:
                return Response({"data" : txt}, status = status.HTTP_400_BAD_REQUEST)
        #()
        '''
        else:
            return Response("Login Failed")
        {"status " : "Login Failed", "data" : serializer.errors}, status = status.HTTP_400_BAD_REQUEST)
        '''
