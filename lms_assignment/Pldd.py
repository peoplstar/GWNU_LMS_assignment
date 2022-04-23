# pip install webdriver-manager # 크롬드라이버 자동설치
# pip install selenium
# pip install bs4
# pip install lxml

from xml.dom.minidom import Element
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException # 예외지정
from selenium.webdriver.chrome.service import Service # 추가
from webdriver_manager.chrome import ChromeDriverManager # 추가
from bs4 import BeautifulSoup as bs

import time
import bs4
import json
import re

# Parameter 전송을 위한 Class 선언
class crawling:    
    def __init__(self, userid, password):
        # 로그인
        self.userid = userid
        self.password = password
        
    def craw(self):
        chrome_options = webdriver.ChromeOptions()

        # 브라우저 창 없이 실행
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--start-maximized")
        chrome_options.add_argument("--window-size=1920,1080")

        # Chromedriver 경로 설정
        browser = webdriver.Chrome(service = Service(ChromeDriverManager().install()), options = chrome_options) # 추가
    
        # url 이동
        browser.get("https://portal.gwnu.ac.kr/user/login.face?ssoReturn=https://lms.gwnu.ac.kr")
        
        # id, pw 입력
        
        browser.find_element(By.ID, "userId").send_keys(self.userid) # 추가
        browser.find_element(By.ID, "password").send_keys(self.password) # 추가

        
        # 로그인 완료
        # browser.find_element_by_xpath("/html/body/div/div/div[1]/div/div/div[1]/a").click()
        # browser.find_element(By.XPATH, "/html/body/div/div/div[1]/div/div/div[1]/a").click() # 추가
        WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div/div/div[1]/div/div/div[1]/a"))).click() # 추가

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

        # 과제 정보 가져오기
        for i in subject_list :
            # frame 값 지정
            browser.switch_to.frame('main')

            # 팝업창 삭제
            try :
                WebDriverWait(browser, 2).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[4]/div[1]/button/span[1]"))).click() # 추가
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

            # 수강과목 과제 클릭
            # browser.find_element(By.XPATH, '//*[@id="3"]/ul/li[2]/a').click()
            WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="3"]/ul/li[2]/a'))).click() # 추가


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

            #Num_C = len(title_result)
            #Num = []
            # 딕셔너리 저자용 리스트 생성

            # 첫 화면으로 가기 위한 뒤로가기 두번
            browser.back()
            browser.back()

        # json 파일용 딕셔너리 생성    

        count = len(title_result)
        a_dict = []
        b_dict = {}
        for j in range(count):
            dict_key.insert(j, 'tasks%d' %j)
            if progress_result[j] == "[진행중]" or progress_result[j] == "[진행예정]":
                for i in range(len(dict_key)):
                    temp_dict = {"course" : course_result[i], "title" : title_result[i], "d_day_start" : d_day_start_result[i], "d_day_end" : d_day_end_result[i], "clear" : clear_result[i], "content" : content_result[i]}
                a_dict.append(temp_dict)
            else:
                pass

        b_dict = {"task": a_dict} # key 값 변경

        # JSON 파일 경로 변경
        with open('./assignmentJson/'+ self.userid +'.json', 'w', encoding = "UTF-8") as f : 
            json.dump(b_dict, f, ensure_ascii = False, default = str, indent = 4)

        # 브라우저 종료
        browser.quit()
        return b_dict