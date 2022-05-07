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

data = {}

def timeControl(d_day_end):
    now = datetime.now()
    now = now.strftime('%Y-%m-%d %H:%M')
    now = datetime.strptime(now, '%Y-%m-%d %H:%M')

    return (d_day_end > now) # d_day_end 가 now 보다 과거일 경우 False

def rwJson(key): 
    with open('./assignmentJson/' + key + '.json', 'r+', encoding = "UTF-8") as f: 
        tmp = json.load(f)
        data = tmp
        return len(data['task'])
    
class taskScheduling:
    def access():
        db_url = 'https://lms-assignment-default-rtdb.firebaseio.com/'

        if not firebase_admin._apps:
            cred = credentials.Certificate("Firebase.json")
            firebase_admin.initialize_app(cred, {
                'databaseURL' : db_url
            })
        
        ref = db.reference('')
        dict_key_list = ref.get().keys() # 학번 dictionary's keys
        key_list = list(dict_key_list) # 학번 List 변환
        
        # DB에 저장된 ID와 PW로 크롤링 한 JSON 파일 로딩
        
        for key in key_list:
            task_list = db.reference(key + '/task').get()
            taskCnt = len(list(filter(None, task_list))) # Remove None data in List
            
            for task in range(0, taskCnt):
                r = db.reference(key + '/task/' + str(task) + '/d_day_end') # 과제 별 마감 시간
                timeResult = timeControl(datetime.strptime(r.get(), '%Y-%m-%d %H:%M'))
                
                # 시간 값 비교 해당 과제 삭제
                if timeResult == False:
                    deleteItem = db.reference(key + '/task/' + str(task))
                    deleteItem.delete()
                    taskCnt -= 1
            
            pw = db.reference(key + '/pw').get() # DB id, pw Link
            crawSystem = Pldd.crawling(key, pw)
             
            newTask = crawSystem.craw()
            newTaskCnt = rwJson(key)

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
        
def main():
    taskScheduling.access()
    
if __name__ == "__main__":
    main()
