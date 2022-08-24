# Made by Pr0t0n
import requests
import threading
import random
import string 
from EmailVerification import TOFVerification as EmailVerification
import hashlib
import time
import ctypes
import json
threads = input("Enter amount of threads to use: ")
#EmailVerification.get_email()
#input()
#EmailVerification.search_mail()
#input()
class TOF:
    def __init__(self):
        self.proxies = []
        self.genned_accounts = 0
        self.emails_used = 0
        self.errors_created = 0
        self.promolinksgenerated = 0
        with open('data/proxies.txt', 'r') as data:
            data = data.readlines()
            for proxy in data:
                self.proxies.append(proxy)
        with open("data/config.json", "r+") as config:
            data = config.read()
            config = json.loads(str(data))
            self.emailprov = config['emailprovider']
            del config

    def get_email(self):
        if self.emailprov == "mail.tm":
            self.email, self.password = EmailVerification.get_email()
            return self.email, self.password
        else:
            self.email = EmailVerification.get_email()
            self.emails_used += 1   
            return self.email
    
    @staticmethod
    def search_mail_for_code(email, password=None):
        if password == None:
            code = EmailVerification.search_mail(email)
        else:
            code = EmailVerification.search_mail(email, password)
        return code

    @staticmethod
    def generate_password():
        return ''.join(random.choice(string.ascii_letters) for x in range(int(random.randint(10, 13)))) + random.choice(["!", "?"])
    
    @staticmethod
    def generate_signature(endpoint, oauth):
        oauth = str(oauth)
        oauth = oauth.replace(" ", "")
        sign_this_md5 = f"{endpoint}{oauth}0d88135dd851f81f9601e477b261a137"
        #print(sign_this_md5)
        return hashlib.md5(sign_this_md5.encode()).hexdigest()
    def update_console_headers(self):
        while True:
            ctypes.windll.kernel32.SetConsoleTitleW(f"TOF Promo Generator | Emails Created: {self.emails_used} | Generated TOF Accounts: {self.genned_accounts} | Promo Links Claimed: {self.promolinksgenerated} | Errors: {self.errors_created} | Threads: {threads}")
    @staticmethod
    def get_promo_link():
        pass
    @staticmethod
    def generate_inital_openid():
        openid = ""
        for i in range(15):
            openid += str(random.randint(1, 9))
        return openid
    def create_account(self):
        password = TOF.generate_password()
        password = hashlib.md5(password.encode()).hexdigest()
        proxy = random.choice(self.proxies)
        if self.emailprov == "mail.tm":
            email, passwordd = TOF.get_email()
            if email == "error":
                print("[-]: Overflow mail.tm Error")
                self.errors_created += 1
                return TOF.create_account
        else:
            email = TOF.get_email()
        proxiess = {
            "http": f"http://{proxy}",
            "https": f"http://{proxy}"
        }
        jsonm = json.dumps({
        "account" : email,
        "account_type" : 1,
        "code_type" : 0})
        sign = TOF.generate_signature("/account/sendcode?account_plat_type=113&app_id=a0ca7921668f7d18c096ad85011589fd&lang_type=en&os=3&source=32", jsonm)
        jsonm = str(jsonm)
        jsonm = jsonm.replace(" ", "")
        headers= {
            "content-type": "application/json",
            "Referer": "https://www.toweroffantasy-global.com/",
        }
        try:
            r = requests.post(f"https://aws-na.intlgame.com/account/sendcode?account_plat_type=113&app_id=a0ca7921668f7d18c096ad85011589fd&lang_type=en&os=3&source=32&sig={sign}", data=jsonm, headers=headers, proxies=proxiess)
        except requests.exceptions.ProxyError:
            print("[-]: Proxy Error")
            self.errors_created += 1
            return TOF.create_account()
        try:
            if r.json()['msg'] != "Success":
                print("[-]: Error sending Verification Code!")
                self.errors_created += 1
                return TOF.create_account()
        except Exception:
            print("[-]: Unknown Error Sending Verification Code")
            self.errors_created += 1
            return TOF.create_account()
        print(f"[+]: Sent Verification Code to email ({email})")
        if self.emailprov == "mail.tm":
            code = TOF.search_mail_for_code(email, passwordd)
        else:
            code = TOF.search_mail_for_code(email)
        if code == "error":
            print("[-]: Error Trying to Get Verification Code (email for TOF not found)")
            self.errors_created += 1
            return TOF.create_account()
        code = code.replace("\n", "")
        jsonm2 = json.dumps({
            "verify_code": code,
            "account": email,
            "account_type": 1,
            "password": password
        })
        newsign = TOF.generate_signature("/account/register?account_plat_type=113&app_id=a0ca7921668f7d18c096ad85011589fd&channelid=113&conn=&gameid=29093&lang_type=en&os=3&sdk_version=2.0&source=32", jsonm2)

        jsonm2 = str(jsonm2)
        jsonm2 = jsonm2.replace(" ", "")
        try:
            signup = requests.post(f"https://aws-na-pass.intlgame.com/account/register?account_plat_type=113&app_id=a0ca7921668f7d18c096ad85011589fd&channelid=113&conn=&gameid=29093&lang_type=en&os=3&sdk_version=2.0&source=32&sig={newsign}", data=jsonm2, headers=headers, proxies=proxiess)
        except requests.exceptions.ProxyError:
            print("[-]: Proxy Error")
            return TOF.create_account()
        try:
            if signup.json()['msg'] != "Success":
                self.errors_created += 1
                print("[-]: Error Creating TOF account!")
                return TOF.create_account()
        except Exception:
            self.errors_created += 1
            print("[-]: Unknown Error Creating Account!")
            return TOF.create_account()
        tof_token = signup.json()['token']
        uuid = signup.json()['uid']
        print("[+] Created Tower of Fantasy Account!")
        self.genned_accounts += 1
        file = open("data/TOFtokens.txt", "a+")
        file.write(f"{tof_token}\n")
        file.close()
        return TOF.create_account()
if __name__ == "__main__":
    TOF = TOF()
    for i in range(1):
        threading.Thread(target=TOF.update_console_headers).start()
    for i in range(int(threads)):
        threading.Thread(target=TOF.create_account).start()
        time.sleep(random.uniform(0.5, 3))
   
