# pip install firebase_admin

import json
from time import strptime
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
def timeControl(d_day_end):
    #self.d_day_end = d_day_end
    now = datetime.now()
    now = now.strftime('%Y-%m-%d %H:%M')
    now = datetime.strptime(now, '%Y-%m-%d %H:%M')
    print(f'd_day_end = {d_day_end}')
    diff = d_day_end - now
    print(d_day_end> now) # d_day_end 가 now 보다 과거일 경우 False

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
        d_day_end = db.reference('20171456/task/0/d_day_end').get() # Time key
        d_day_end = datetime.strptime(d_day_end, '%Y-%m-%d %H:%M')
        #print(type(d_day_end)) # Time value
        timeControl(d_day_end)
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
