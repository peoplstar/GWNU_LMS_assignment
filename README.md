
# GWNU Assignment PUSH Notice
### `Gangneung-Wonju National University Assignment PUSH NOTICE`   

* 현재 우리 학교에는 과제에 대한 알림 시스템은 이메일을 통해 받거나, 직접 URL에 접속하여
  확인 해야한다.

* 위와 같은 방법은 번거로울 뿐 더러, 가독성도 좋지 않아 개발하게 되었다.

* 해결법으로는 모바일에서 API를 통한 ID와 PW를 POST 메소드로 서버에서 전송하면 해당 데이터를 통해 크롤링을 통해 접속을 시도한다.

* 각 강의에 대한 HTML Tag 값을 이용해 리스트에 저장하여 모든 과목명, 과제명, 과제 내용, 기한 등을 저장한다.

* 해당 내용을 JSON 파일로 변환하여 파싱을 통해 DB에 저장한다.

* 모바일에서 GET 메소드를 보낼 시 DB에서 과제에 대한 모든 내용을 서버에서 Response한다.


  작업자   | 역할        |
  :-----: | :----------:|
  김중원        | Kotlin       | 
  최민규, 윤한을 | Server, DB   | 
  김종원, 신현준 | Crawling |


> ### Django 서버 구축

`pip install django` : django 패키지 설치

`pip install djangorestframework` : REST API를 위한 REST Framework 설치

`django-admin startproject [projectname]` : django 프로젝트 생성

`python3 manage.py start app [appname]` : django app 생성

* 필자는 `api_app`으로 생성했습니다.

`pip install chromedriver-autoinstaller`

* <a href = https://tttap.tistory.com/221>크롬 설치 </a>

`pip install -U urllib3 requests` : requests & responses 를 위한 설치


> ### models.py 설정

```python
from django.db import models

# Create your models here.
class lmsItem(models.Model):
    lms_id = models.CharField(max_length = 15, primary_key = True)
    lms_pw = models.CharField(max_length = 30)
    # FirebaseToken = models.CharField(max_length = )
```

* 우리는 학교 로그인 정보를 받아서 크롤링을 진행할 것이기에 필요한 API로 받을 정보는 ID와 PW이기에 위와 같은 설정을 하고, 기본 키가 되는 것은 ID 이기에 `primary_key = True`로 설정했다.

* 이후, Firebase FCM PUSH를 위한 FirebaseToken을 받아야 하므로 주석으로 처리했다.

> ### Settings.py 설정


Settings.py의 경로는 `[projectname]/[projectname]/settings.py` 에서 확인 가능하다.


<img src=https://user-images.githubusercontent.com/78135526/164878910-929d5d98-77d2-453b-9ced-e0ce22ca4cf1.png width = '250' height = '250'>


Default는 `ALLOWED_HOSTS = []`로 되어 있다. 이렇게 되면 외부에서 접근이 불가능하다. 해당 서버에 모두가 접근 할 수 있게 위와 같이 **'*'** 로 설정하고, 추후 AWS 인바운드 정책 및 iptables로 보안을 설정 할 것이다.

INSTALLED_APPS는 REST API를 사용하기 위해 `rest_framework` 명시, 우리가 사용할 앱 `api_app`을 명시해준다.

> ### Views.py 파일 수정

```python
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
            txt = crawSystem.craw()

            # JSON DB data processing
            firedb = firebaseLink.DBLink(userid)
            firedb.rwJson()
            firedb.Link()
            return Response(txt)
        #({"status" : "success", "data" : serializer.data}, status = status.HTTP_200_OK)
        else:
            return Response("Login Failed")
        #{"status " : "Login Failed", "data" : serializer.errors}, status = status.HTTP_400_BAD_REQUEST)
```
* ID와 PW는 평문으로 API Server에 저장된다면 보안상 매우 취약하게 되므로, `serializer.save()`를 주석 처리하여 저장되지 않게 명시한다. 

  * ##### *추후 https를 이용해 보완*   

* FireBase와 연동을 위해 `firebaseLink`를 import 하고, 파싱된 userid를 매개변수로 넘겨 DB에 Assignmnet data를 저장한다.
   
* 모바일과의 통신으로부터 얻은 ID와 PW를 python 객체로 얻기 위해 `dumps`와 `loads`를 동시에 사용한다.

* JSON은 **{key : value}** 로 이루어져 있는 파일의 형태이기 때문에 key로 접근이 가능하다.

> ### Crawling
```python
# Parameter 전송을 위한 Class 선언
class crawling:    
    def __init__(self, userid, password):
        # 로그인
        self.userid = userid
        self.password = password
        
    def craw(self):
        chrome_options = webdriver.ChromeOptions()

        # 브라우저 창 없이 실행
```
* 별도의 클래스로 지정해주지 않아 `views.py`로 받은 ID와 PW를 넘기기 위해 위 처럼 수정을 해줬다.

> ### FirebaseLink.py
```python
# pip install firebase_admin

import json
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from firebase_admin import db

# Firebase database 인증 및 앱 초기화

data = {}

class DBLink:
    def __init__(self, userid):
        # 로그인
        self.userid = userid
   
    def rwJson(self):
        # 윈도우 경로 : r'lms_assignment/'
        # 리눅스 경로 : './assignmentJson/' 
        with open('./assignmentJson/' + self.userid + '.json', 'r+', encoding = "UTF-8") as f: 
            tmp = json.load(f)
            data[self.userid] = tmp
    
    def Link(self):
        db_url = 'https://lms-assignment-default-rtdb.firebaseio.com/'

        if not firebase_admin._apps:
            cred = credentials.Certificate("firebase.json")
            firebase_admin.initialize_app(cred, {
                'databaseURL' : db_url
            })

        # 학번이 있는지 확인, 이후 db.reference('학번') 으로 JSON Response
        ref = db.reference('')
        ref.update({self.userid : data[self.userid]})
```

<p align="center">
<img src=https://user-images.githubusercontent.com/78135526/164879401-366ad8ec-8c0a-41f6-8861-6e89164439fd.png width = 500 height = 230>
</p>

* DB에서 모든 학생의 과제 정보를 가지고 있어야 하기에 그에 맞은 키를 주기 위해 받은 userid를 key로 설정하고 크롤링으로 부터 받은 JSON을 value로 저장한다.


> ### TaskScheduling.py
```python
data = {}

def timeControl(d_day_end):
    now = datetime.now()
    now = now.strftime('%Y-%m-%d %H:%M')
    now = datetime.strptime(now, '%Y-%m-%d %H:%M')

    return (d_day_end > now) # d_day_end 가 now 보다 과거일 경우 False
```

* DB에 저장되어 있는 D_day_end의 시간과 현재 시간을 비교하여 미리 종료가 된 과제의 경우 False를 Return하여 로직을 수행한다.

```python
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
```

* `timeControl`로 수행한 결과 값을 토대로 해당 과제를 delete하는 경우 그 위치의 List Item는 None으로 초기화 되기에 `taskCnt = len(list(filter(None, task_list)))` Filter() 함수를 이용하여 None을 지운다.