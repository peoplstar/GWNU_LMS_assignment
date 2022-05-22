# pip install webdriver-manager # 크롬드라이버 자동설치
# pip install selenium
# pip install bs4
# pip install lxml

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException # 예외지정
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import UnexpectedAlertPresentException as PE # 팝업 예외 지정
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup as bs
from xml.dom.minidom import Element
from firebase_admin import credentials
from firebase_admin import firestore
from firebase_admin import db
import firebase_admin
import time
import bs4
import json
import base64
import rsa 

# def decryptionMsg(encrypted_msg):
#     encoded_msg = base64.b64decode(encrypted_msg) 
#     keyType = './private_key.pem'
#     private_key_bytes = open(keyType, 'rb').read()
#     private_key = rsa.PrivateKey.load_pkcs1(keyfile = private_key_bytes)
#     msg = rsa.decrypt(encoded_msg, private_key).decode('utf-8')
#     return msg

# Parameter 전송을 위한 Class 선언
class crawling:    
    def __init__(self, userid, password, token = None):
        # 로그인
        self.userid = userid
        self.password = password
        self.token = token
        
    def craw(self):
        chrome_options = webdriver.ChromeOptions()

        # 브라우저 창 없이 실행
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument("--disable-gpu")  # 추가
        chrome_options.add_argument("--disable-infobars") # 추가
        chrome_options.add_argument("--disable-extensions") # 추가
        chrome_options.add_argument("--disable-popup-blocking") # 추가
        # 오류제어 추가
        chrome_options.add_argument("--no-sandbox")  # 대부분의 리소스에 대한 액세스를 방지 추가
        chrome_options.add_argument("--disable-setuid-sandbox") # 크롬 충돌을 막아줌 추가 
        chrome_options.add_argument("--disable-dev-shm-usage") # 메모리가 부족해서 에러가 발생하는 것을 막아줌 추가
        
        # Chromedriver 경로 설정
        browser = webdriver.Chrome(service = Service(ChromeDriverManager().install()), options = chrome_options) # 추가
    
        # url 이동
        browser.get("https://lms.gwnu.ac.kr/Main.do?cmd=viewHome&userDTO.localeKey=ko")  # 변경

        # decryptionPassword = decryptionMsg(self.password)
        # print(decryptionPassword)
        # id, pw 입력 기존 방식과 다른 붙여넣기 방식으로 입력
        browser.execute_script("arguments[0].value=arguments[1]", browser.find_element(By.ID, "id"), self.userid) # 추가
        browser.execute_script("arguments[0].value=arguments[1]", browser.find_element(By.ID, "pw"), self.password) # 추가

        # 로그인 버튼 클릭
        WebDriverWait(browser, 3).until(EC.element_to_be_clickable((By.XPATH, "//*[@id='loginForm']/fieldset/p[2]/a"))).click() # 변경

        # 계정 정보가 일치하지 않을 시 예외처리 추가
        alert_result = ""

        try :
            WebDriverWait(browser, 0.1).until(EC.alert_is_present()) 
            alert = browser.switch_to.alert
            alert_result = alert.text
            alert.accept()
        except :
            pass

        if alert_result == "입력하신 아이디 혹은 비밀번호가 일치하지 않습니다." :
            print("입력하신 아이디 혹은 비밀번호가 일치하지 않습니다.")
            # 계정정보가 동일하지 않을 시 파이썬 종료
            browser.close()
            return "Login Failed"
        else:
            # 현재 수강 과목 리스트로 저장 (최대 8개)
            subject_list = ['//*[@id="mCSB_1_container"]/li[1]/a/span[1]',
                            '//*[@id="mCSB_1_container"]/li[2]/a/span[1]',
                            '//*[@id="mCSB_1_container"]/li[3]/a/span[1]',
                            '//*[@id="mCSB_1_container"]/li[4]/a/span[1]',
                            '//*[@id="mCSB_1_container"]/li[5]/a/span[1]',
                            '//*[@id="mCSB_1_container"]/li[6]/a/span[1]',
                            '//*[@id="mCSB_1_container"]/li[7]/a/span[1]',
                            '//*[@id="mCSB_1_container"]/li[8]/a/span[1]']


            # 과제에 대한 리스트 선언
            title_result = []
            d_day_start_result = []
            d_day_end_result = []
            content_result = []
            d_end_result = []
            course_result = []
            clear_result = []
            progress_result = []

            # json 리스트 선언
            dict_key = []
            temp_dict = {}

            a_dict = []
            b_dict = {}

            # 과제 정보 가져오기
            for i in subject_list :
            
                # 팝업창 삭제
                try :
                    browser.find_element((By.XPATH, "/html/body/div[4]/div[1]/button/span[1]")).click() # 추가
                except :
                    pass
                
                # 리스트에 없는 과목 예외처리
                try :
                    searching = browser.find_element(By.XPATH, i)
                except :
                    print("모든 과제를 불러왔습니다.")
                    break
                
                # 수강과목 클릭
                searching.click()
                try : 
                    WebDriverWait(browser, 0.2).until(EC.alert_is_present())
                    alert = browser.switch_to.alert
                    alert.accept()
                    continue
                except :        
                    try :
                        # 수강과목 과제 클릭
                        WebDriverWait(browser, 2).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="3"]/ul/li[2]/a'))).click() # 추가
                        time.sleep(3)
                        # 수강과목 이름,과제내용 가져오기
                        source = browser.page_source
                        bs = bs4.BeautifulSoup(source, 'lxml')

                        # 과제제목 크롤링
                        titles = bs.find_all('h4','f14')
                        # 제출기한 크롤링
                        d_days = bs.find_all('table','boardListInfo')
                        # 제출기한 시작과 끝 분할
                        slice1 = slice(16)
                        slice2 = slice(19, 35)
                        # 과제내용 크롤링
                        contents = bs.find_all('div','cont pb0')
                        # 과목이름 크롤링
                        course = bs.find('h1','f40')
                        # 과제진행여부 크롤링 추가
                        progresses = bs.find_all('span','f12')

                        # 과제제목 저장, 과목이름 저장
                        for title in titles:
                            title_result.append(title.get_text().strip().replace("\t","").replace("\n","").replace("\xa0",""))
                            course_result.append(course.get_text().replace("\t","").replace("\n","").replace("\xa0",""))

                        # 제출기한 시작 저장
                        for d_day_start in d_days:
                            d_day_start_result.append(d_day_start.get_text().replace("\t","").replace("\n","").replace("\xa0","").replace("과제 정보 리스트제출기간점수공개일자연장제출제출여부평가점수","")[slice1])

                        # 제출기한 끝 저장
                        for d_day_end in d_days:
                            d_day_end_result.append(d_day_end.get_text().replace("\t","").replace("\n","").replace("\xa0","").replace("과제 정보 리스트제출기간점수공개일자연장제출제출여부평가점수","")[slice2])

                        # 제출여부 저장
                        for clear in d_days:
                            clear_result.append(clear.get_text().replace("\t","").replace("\n","").replace("\xa0","")
                                                                .replace("과제 정보 리스트제출기간점수공개일자연장제출제출여부평가점수","")
                                                                .replace("1","").replace("2","").replace("3","").replace("4","")
                                                                .replace("5","").replace("6","").replace("7","").replace("8","")
                                                                .replace("9","").replace("0","").replace("-","").replace(".","")
                                                                .replace("~","").replace(":","").replace(" ","").replace("(","")
                                                                .replace(")","").replace("미허용","").replace("허","").replace("용",""))

                        # 과제내용 저장
                        for content in contents:
                            content_result.append(content.get_text().replace("\t","").replace("\n","").replace("\xa0",""))


                        # 과제진행여부 저장 추가
                        for progress in progresses:
                            progress_result.append(progress.get_text().replace("\t","").replace("\n","").replace("\xa0",""))

                        def getprogress(ch):
                            if ch == "[진행중]" or ch == "[마감]" or ch == "[진행예정]":
                                return True
                            else:
                                return None

                        progress_result = list(filter(getprogress, progress_result)) 

                        # 첫 화면으로 가기 위한 뒤로가기 두번
                        browser.back()
                        browser.back()
                    except :
                        continue
                    continue
                
            # json 파일용 딕셔너리 생성
            count = len(title_result)

            for j in range(count):
                dict_key.insert(j, 'tasks%d' %j)
                if progress_result[j] == "[진행중]" or progress_result[j] == "[진행예정]":
                    for i in range(len(dict_key)):
                        temp_dict = {"course" : course_result[i], "title" : title_result[i], "d_day_start" : d_day_start_result[i], "d_day_end" : d_day_end_result[i], "clear" : clear_result[i], "content" : content_result[i]}
                    a_dict.append(temp_dict)
                else:
                    pass
                
            b_dict = {"task" : a_dict}
            b_dict["pw"] = self.password 
        
            if self.token == None:
                db_url = 'https://lms-assignment-default-rtdb.firebaseio.com/'

                if not firebase_admin._apps:
                    cred = credentials.Certificate("./lms-assignment-firebase-adminsdk-gg9hv-0e2b022f8b.json")
                    firebase_admin.initialize_app(cred, {
                        'databaseURL' : db_url
                    })
                    
                self.token = db.reference(self.userid + '/token').get()
                b_dict["token"] = self.token
            else:
                pass
            
            with open('./assignmentJson/'+ self.userid +'.json', 'w+', encoding = "UTF-8") as f : 
                json.dump(b_dict, f, ensure_ascii = False, default = str, indent = 4)


            # 브라우저 종료
            browser.close()
            return b_dict