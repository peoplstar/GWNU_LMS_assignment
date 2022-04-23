# pip install firebase_admin

import json
import firebase_admin
import Pldd
from firebase_admin import credentials
from firebase_admin import firestore
from firebase_admin import db
from datetime import datetime
# 오전 6시 Crawling
# 비교 전 제출 기한 over delete
# Firebase ID / PW 접근 후 Pldd
# DB & JSON 비교
def timeControl():
    now = datetime.now()
    print(now.strftime('%Y-%m-%d %H:%M:%S'))
    # return 타임 비교 값
    
class taskScheduling:
    def access():
        db_url = 'https://lms-assignment-default-rtdb.firebaseio.com/'

        if not firebase_admin._apps:
            cred = credentials.Certificate("Firebase.json")
            firebase_admin.initialize_app(cred, {
                'databaseURL' : db_url
            })
        
        ref = db.reference('')
        key_list = (ref.get().keys()) # 학번만 출력 ref.get().keys()
        # timeControl()
        d_day_end = db.reference('20171473')
        print(d_day_end)
        '''
        for id in key_list:
            userid = db.reference(id + '/passwd')   
            passwd = userid.get() # 복호화 과정 필요
            
            craws = Pldd.crawling(userid, passwd)
            craws.craw()
            
            
            Crawling 된 JSON을 Firebase와 비교
            '''
            # print(f'userid : {id} passwd : {passwd}')
            
            
            
if __name__ == "__main__":
    taskScheduling.access()
