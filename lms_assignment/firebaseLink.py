# pip install firebase_admin

import json
from lib2to3.pgen2 import token
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from firebase_admin import db

# Firebase database 인증 및 앱 초기화

data = {}

class DBLink:
    def __init__(self, userid, token):
        # 로그인
        self.userid = userid
        self.token = token
        
    def rwJson(self):
        # 윈도우 경로 : r'lms_assignment/'
        # 리눅스 경로 : './assignmentJson/' 
        with open('./assignmentJson/' + self.userid + '.json', 'r+', encoding = "UTF-8") as f: 
            tmp = json.load(f)
            data[self.userid] = tmp
    
    def Link(self): 
        db_url = 'https://lms-assignment-default-rtdb.firebaseio.com/'

        if not firebase_admin._apps:
            cred = credentials.Certificate("./lms-assignment-firebase-adminsdk-gg9hv-0e2b022f8b.json")
            firebase_admin.initialize_app(cred, {
                'databaseURL' : db_url
            })

        # 학번이 있는지 확인, 이후 db.reference('학번') 으로 JSON Response
        ref = db.reference('')
        ref.update({self.userid : data[self.userid]})
        
    def TokenUpdate(self): 
        db_url = 'https://lms-assignment-default-rtdb.firebaseio.com/'

        if not firebase_admin._apps:
            cred = credentials.Certificate("./lms-assignment-firebase-adminsdk-gg9hv-0e2b022f8b.json")
            firebase_admin.initialize_app(cred, {
                'databaseURL' : db_url
            })
            
        ref = db.reference(self.userid)
        ref.update({'token' : self.token})
