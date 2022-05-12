from pyfcm import FCMNotification
 
APIKEY = "AAAAmflPfQQ:APA91bEuJalspiK5RlQ-x5LN1zgpcfhO3mZNbDRMIf-DuuksI8zDGwduvMEpjk8-45sj06AnOMyoDL7CEYx-G3lFVj-UM5Kp2RQQzQxfzOBg5D0JRgQv8CjqEoOM7nkY7usEit5YZLK6"
 
# 파이어베이스 콘솔에서 얻어 온 서버 키를 넣어 줌
push_service = FCMNotification(APIKEY)
 
def sendMessage(self, body, title, token):
    # 메시지 (data 타입)
    self.token = token
    
    data_message = {
        "body" : body,
        "title" : title
    }
 
    # 토큰값을 이용해 1명에게 푸시알림을 전송함
    push_service.single_device_data_message(registration_id = self.token, data_message = data_message)