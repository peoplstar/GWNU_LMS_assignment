
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
  김중원 | Kotlin       | 
  최민규 | Server       | 
  김종원, 신현준 | Crawling |

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
            crawSystem.craw()
            return Response("Login Success")
        #({"status" : "success", "data" : serializer.data}, status = status.HTTP_200_OK)
        else:
            return Response("Login Failed")
        #{"status " : "Login Failed", "data" : serializer.errors}, status = status.HTTP_400_BAD_REQUEST)
```
* ID와 PW는 평문으로 API Server에 저장된다면 보안상 매우 취약하게 되므로, `serializer.save()`를 주석 처리하여 저장되지 않게 명시한다. 

  * ##### *추후 https를 이용해 보완*   
   
* 모바일과의 통신으로부터 얻은 ID와 PW를 python 객체로 얻기 위해 `dumps`와 `loads`를 동시에 사용한다.

* JSON은 **{key : value}** 로 이루어져 있는 파일의 형태이기 때문에 key로 접근이 가능하다.

* 