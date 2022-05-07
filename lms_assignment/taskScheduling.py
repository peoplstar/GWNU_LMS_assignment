# pip install firebase_admin

import json
from time import strptime
from turtle import st
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

    return (d_day_end > now) # d_day_end 가 now 보다 과거일 경우 False

    # return 타임 비교 값
    
class taskScheduling:
    def access():
        db_url = 'https://lms-assignment-default-rtdb.firebaseio.com/'

        if not firebase_admin._apps:
            cred = credentials.Certificate("./lms-assignment-firebase-adminsdk-gg9hv-0e2b022f8b.json")
            firebase_admin.initialize_app(cred, {
                'databaseURL' : db_url
            })
        
        ref = db.reference('')
        dict_key_list = ref.get().keys() # 학번 dictionary's keys
        key_list = list(dict_key_list) # 학번 List 변환
        task_list = db.reference(key_list[0] + '/task').get()

        for task in range(0, len(task_list)):
            r = db.reference(key_list[0] + '/task/' + str(task) + '/d_day_end') # 과제 별 마감 시간
            timeResult = timeControl(datetime.strptime(r.get(), '%Y-%m-%d %H:%M')) # 과제 마감 시간
            
            # 시간 값 비교 해당 과제 삭제
            if timeResult == False:
                deleteItem = db.reference(key_list[0] + '/task/' + str(task))
                print(f'Time Result == {timeResult}')
                deleteItem.delete()
                

        # d_day_end = db.reference('20171456/task/0/d_day_end').get() # Time key
        # d_day_end = datetime.strptime(d_day_end, '%Y-%m-%d %H:%M')
        # print(type(d_day_end)) # Time value
        # timeControl(d_day_end)
        
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
