from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import lmsItemSerializer
from .models import lmsItem
from selenium.common.exceptions import UnexpectedAlertPresentException as PE # 로그인 오류
from firebase_admin import credentials
from firebase_admin import firestore
from firebase_admin import db
import Pldd
import json
import firebaseLink
import firebase_admin

# from .models import assignment
# Create your views here.

def isNone(r):
    if r.get() == None:
        return 'isNone'
    else:
        return 'isNotNone'
    
class lmsItemViews(APIView):
    '''
    def get(self, request, lms_id):
        return(RSA 공개키를 전달)
    '''

    def post(self, request):
        serializer = lmsItemSerializer(data = request.data)
        if serializer.is_valid():
            # serializer.save()

            ref = db.reference('')
            dict_key_list = ref.get().keys() # 학번 dictionary's keys
            key_list = list(dict_key_list) # 학번 List 변환
            inform = request.data
            dump = json.dumps(inform)
            tmp = json.loads(dump)
            userid = tmp['lms_id']
            password = tmp['lms_pw']
            db_url = 'https://lms-assignment-default-rtdb.firebaseio.com/'

            if not firebase_admin._apps:
                cred = credentials.Certificate("./lms-assignment-firebase-adminsdk-gg9hv-0e2b022f8b.json")
                firebase_admin.initialize_app(cred, {
                    'databaseURL' : db_url
                })
                
            ref = db.reference(userid)
            if isNone(ref) == isNone:
                # Crawling Method Parameter 
                crawSystem = Pldd.crawling(userid, password)
                
                try :
                    txt = crawSystem.craw()
                    status_code = 200
                except PE :
                    txt = 'Login Failed'
                    status_code = 400
            else:
                r = ref.child('task')
                txt = r.get()
            
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
