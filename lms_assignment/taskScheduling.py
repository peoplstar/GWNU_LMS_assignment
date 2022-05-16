# pip install firebase_admin

import json
from time import strptime
import firebase_admin
import Pldd
import push_fcm_notification
import firebaseLink
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

def newTaskCrawlingCnt(key): 
    with open('./assignmentJson/' + key + '.json', 'r+', encoding = "UTF-8") as f: 
        tmp = json.load(f)
        data = tmp
        return len(data['task'])

def isNone(r):
    if r.get() == None:
        return 'isNone'
    else:
        return 'isNotNone'

    
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
        
        # DB에 저장된 ID와 PW로 크롤링 한 JSON 파일 로딩     
        
        for key in key_list:
            task_list = db.reference(key + '/task').get()
            taskCnt = len(list(task_list))
            
            for task in range(0, taskCnt):
                r = db.reference(key + '/task/' + str(task) + '/d_day_end') # 과제 별 마감 시간
                if isNone(r) == 'isNone': # 삭제 이후 과제 번호가 없으면 None 값
                    taskCnt -= 1
                    continue
                else:
                    timeResult = timeControl(datetime.strptime(r.get(), '%Y-%m-%d %H:%M'))
                    if timeResult == False: # 시간 값 비교 해당 과제 삭제
                        deleteItem = db.reference(key + '/task/' + str(task))
                        deleteItem.delete()
                        taskCnt -= 1
            
            pw = db.reference(key + '/pw').get()
            crawToken = None
            crawSystem = Pldd.crawling(key, pw, crawToken)  
            crawSystem.craw()
            newTaskCnt = newTaskCrawlingCnt(key)
            
            if newTaskCnt != taskCnt:
                token = db.reference(key + '/token').get()
                push_fcm_notification.sendMessage("강릉원주대학교 과제", "새로운 과제가 등록 되었습니다.", token)
                firedb = firebaseLink.DBLink(key)
                firedb.rwJson()
                firedb.Link()

def main():
    taskScheduling.access()
    
if __name__ == "__main__":
    main()
