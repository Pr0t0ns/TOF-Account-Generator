from distutils.log import error
from random import random
import string
import time
import httpx
import requests
import base64
import json
import random
with open("data/config.json", "r") as conf:
    data = conf.read()
    data = json.loads(str(data))
    provider = data['emailprovider']
    del data
codes = []
proxies = []
with open("data/proxies.txt", 'r+') as proxyy:
    data = proxyy.readlines()
    for proxy in data:
        proxies.append(proxy)
proxiess = {
    "http://": f"http://{proxy}",
    "https://": f"http://{proxy}"
}
# THE EMAIL.TM API WRAPPER WAS NOT MADE BY ME!!!
class Base:
      URL              =  'https://api.mail.tm'
      GET_TOKEN        = ('%s/token' % (URL),    'POST')
      GET_DOMAINS      = ('%s/domains' % (URL),  'GET')
      CREATE_ACCOUNT   = ('%s/accounts' % (URL), 'POST')
      GET_MESSAGES     = ('%s/messages' % (URL), 'GET')
class Email:
    def __init__(self):
          self.emails  = []
          self.session = requests.Session()
          self.session.proxies = {
                "http://": f"http://{proxy}",
                "https://": f"http://{proxy}"
          }

    def getUsername(self):
        return ''.join(random.choice(string.ascii_lowercase) for _ in range(10))

    def getPassword(self):
        return ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(15))

        
    def getEmail(self):
        email    = self.getUsername() + '@' + "arxxwalls.com"
        password = self.getPassword()
        try:
            return self.session.post(
                        Base.CREATE_ACCOUNT[0],
                        json = {
                            'address'  : email,
                            'password' : password,
                        },
                        proxies=proxiess
            ).json(), email, password
        except Exception:
            return "error", "error", "error"
    def getToken(self, email, password):
        try:
            return self.session.post(
                    Base.GET_TOKEN[0],
                    headers = {'Content-Type': 'application/json'},
                    json    = {
                            'address'  : email,
                            'password' : password,
                    },
                    proxies=proxiess
            ).json()
        except Exception:
            return "error"
        
    def getEmailInbox(self, emailToken):
        try:
            return requests.get(
                    Base.GET_MESSAGES[0],
                    headers = {
                            'Authorization': 'Bearer %s' % (
                                            emailToken
                            )
                    },
                    proxies=proxiess
            ).json()
        except Exception:
            return "error"
    def getMessageFromId(self, emailToken, messageId):
        try:
          return requests.get(
                 f'https://api.mail.tm/messages/{messageId}',
                    headers = {
                            'Authorization': 'Bearer %s' % (
                                              emailToken
                            )
                    },
                    proxies=proxiess
          ).json()
        except Exception:
            return "error"
Email = Email()
class TOFVerification:

    @staticmethod
    def get_email():
        if provider == "xitroo.com":
            return ''.join(random.choice(string.ascii_lowercase) for x in range(int(random.randint(10, 16)))) + "@xitroo.com"
        elif provider == "guilded.lol":
            return ''.join(random.choice(string.ascii_lowercase) for x in range(int(random.randint(10, 16)))) + "@guilded.lol"
        elif provider == "mail.tm":
            data, email, password = Email.getEmail()
            if data == "error":
                return "error", "error"
            return email, password
        elif provider == "hcaptchasolver.online":
            return ''.join(random.choice(string.ascii_lowercase) for x in range(int(random.randint(10, 16)))) + "@hcaptchasolver.online"
    @staticmethod
    def search_mail(email, password=None):
        retries = 0
        print("[?]: Checking Email For Verification Code")
        code_html = ""
        proxy = random.choice(proxies)

        if provider == "xitroo.com":
            while retries != 8:
                time.sleep(2)
                try:
                    data = httpx.get(f"https://api.xitroo.com/v1/mails?locale=en&mailAddress={email}&mailsPerPage=25&minTimestamp=0&maxTimestamp={int(time.time())}")
                except httpx.ReadTimeout:
                    print("[+]: Xitroo.com Doesn't seem to be working!")
                    return "error"
                try:
                    mail_id = data.json()['mails'][0]["_id"]
                    break
                except Exception:
                    retries += 1
            if retries == 8:
                return "error"
            mail_body = httpx.get(f"https://api.xitroo.com/v1/mail?locale=en&id={mail_id}")
            code_html = mail_body.json()['bodyText']
            code_text = base64.b64decode(code_html)
            code_text = code_text.decode('utf-8')
            code_text = code_text.replace(" ", "")
            code_text = code_text[:407]
            code_text = code_text[:235]
            code_text = code_text[115:]
            code_text = code_text.replace("Youarereceivingthis", "")
            code_text = code_text.replace(" ", "")
            print(f"[+]: Recieved Verification Code ({code_text[:6]})")
            return code_text[:6]
        elif provider == "guilded.lol":
            headers = {
                "user-agent": "noratelimit",
            }
            while retries != 8:
                time.sleep(2)
                url = f'https://asari.gay/api/v1/emails/{email}'
                data = httpx.get(url, headers=headers)
                try:
                    code_html = data.json()['emails'][0]['body']
                    break
                except IndexError:
                    retries += 1
            if code_html == "":
                return "error"
            code_html = code_html.replace("\n", "")
            code_html = code_html.replace(" ", "")
            code_text = code_html[:407]
            code_text = code_text[:235]
            code_text = code_text[100:]
            code_text = code_text.replace("r300seconds:*", "")
            code_text = code_text.replace("YouarereceivingthisautomaticallygeneratedemailtohelpyouregisteremailaddresswithyourTowerofFantasyaccount.Ifyoudidn'te", "")
            print(f"[+]: Recieved Verification Code ({code_text})")
            return code_text
        elif provider == "mail.tm":
            token = Email.getToken(email, password)
            if token == "error":
                return "error"
            token = token['token']
            while retries != 8:
                time.sleep(2)
                contents = Email.getEmailInbox(token)
                if contents == "error":
                    return "error"
                try:
                    id = contents['hydra:member'][0]['id']
                    break
                except Exception:
                    retries += 1
            contentss = Email.getMessageFromId(token, id)
            if contentss == "error":
                return "error"
            code = contentss['html']
            code = str(code)
            code = code[:1859]
            code = code[1844:]
            code = code.replace(" ", "")
            code = code.replace("\n", "")
            print(f"[+]: Recieved Verification Code ({code})")
            return code
