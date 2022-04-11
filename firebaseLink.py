# pip install firebase_admin

import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

# Firebase database 인증 및 앱 초기화
cred = credentials.Certificate("lms-assignment-firebase-adminsdk-gg9hv-0e2b022f8b.json")


