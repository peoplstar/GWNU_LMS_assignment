from pyfcm import FCMNotification
 
APIKEY = "Your Server Key"
 
# 파이어베이스 콘솔에서 얻어 온 서버 키를 넣어 줌
push_service = FCMNotification(APIKEY)
 
def sendMessage(body, title, local_token):
    # 메시지 (data 타입)
    global token
    token = local_token
    
    data_message = {
        "body": body,
        "title": title
    }
 
    # 토큰값을 이용해 1명에게 푸시알림을 전송함
    result = push_service.single_device_data_message(registration_id = token, data_message = data_message)
 
 
sendMessage("강릉원주대학교 과제", "새로운 과제가 등록 되었습니다.")