from cryptography.fernet import Fernet as fn

# key = fn.generate_key() 키 생성

# with open('./key.pem', 'wb') as f:
#     f.write(key)
def load_key():
    """
    Load the previously generated key
    """
    return open('./key.pem', 'rb').read()

class De_Encryption():
    def __init__(self, msg):
        self.msg = msg
        self.key = load_key()
        
    def encryption(self):
        
        cipher_suite = fn(self.key)

        cipher_text = cipher_suite.encrypt(self.msg.encode())
        
        return cipher_text
        
    def decryption(self):
        self.msg = self.msg.encode()
        cipher_suite = fn(self.key)
        
        print(self.msg)
        
        plain_text = cipher_suite.decrypt(self.msg).decode()            
        
        return plain_text


# if __name__ == '__main__': # TEST
#     msg = '11'
#     de = De_Encryption(msg)
#     en_msg = de.encryption()
#     en = De_Encryption(en_msg)
#     en.decryption()