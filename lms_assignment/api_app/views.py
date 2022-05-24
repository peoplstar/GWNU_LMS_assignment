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

def DataLink(userid, token):
    # JSON DB data processing
    firedb = firebaseLink.DBLink(userid, token)
    firedb.rwJson()
    firedb.Link()
    firedb.TokenUpdate()
    
class lmsItemViews(APIView):
    # def get(self, request):

    #     return Response(publicKey, status = status.HTTP_200_OK)

    def post(self, request):
        serializer = lmsItemSerializer(data = request.data)
        if serializer.is_valid():
            # serializer.save()

            inform = request.data
            dump = json.dumps(inform)
            tmp = json.loads(dump)
            userid = tmp['lms_id']
            password = tmp['lms_pw']
            token = tmp['token']
            db_url = 'https://lms-assignment-default-rtdb.firebaseio.com/'
    
            txt = ""
            result = {}
            
            if not firebase_admin._apps:
                cred = credentials.Certificate("./lms-assignment-firebase-adminsdk-gg9hv-0e2b022f8b.json")
                firebase_admin.initialize_app(cred, {
                    'databaseURL' : db_url
                })
            
            ref = db.reference(userid)
            
            if isNone(ref) == 'isNone':
                # Crawling Method Parameter
                crawSystem = Pldd.crawling(userid, password, token)
                msg = crawSystem.login()
                if msg != "":
                    txt = 'Login Failed'
                    return Response({"data" : txt}, status = status.HTTP_400_BAD_REQUEST)
                else:
                    msg = crawSystem.craw()
                    msg = msg['task']

            else:
                ref.update({'token' : token})
                r = ref.child('task')
                msg = r.get()
            

            DataLink(userid, token)

            result['task'] = msg
            
            return Response(result, status = status.HTTP_200_OK)

