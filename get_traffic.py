import requests
import threading
import base64
from os import environ

username = environ.get('username', 'admin')
password = environ.get('password', 'admin')
domain = environ.get('domain', '192.168.1.1')
token = ''
login_authorization = base64.b64encode('{username}:{password}'.format(username=username,password=password).encode('utf-8') ).decode("utf-8")
print(login_authorization)

def getToken(username=username, password=password):
    formData = {
        "group_id":"",
        "action_mode":"",
        "action_script":"",
        "action_wait":"5",
        "current_page":"Main_Login.asp",
        "next_page":"Main_Login.asp",
        "login_authorization": login_authorization,
        "cloud_file":"",
        "login_username":username,
        "login_passwd":password
    }
    print(formData)
    r = requests.post('http://{domain}/login.cgi'.format(domain=domain), formData)
    print(r.cookies)
    print(r.content)
    cookies = requests.utils.dict_from_cookiejar(r.cookies)
    print(cookies['asus_token'])
    global token
    token = cookies['asus_token']


def getTraffic():
    if token == '':
        getToken()
    # '''
    header_cookie = 'asus_token={token}; traffic_warning_0=2017.10:1'.format(token=token)
    headers = {'cookie': header_cookie}
    r = requests.get('http://192.168.1.1/getTraffic.asp', headers=headers)
    # print(r.status_code)
    # print(r.headers['content-type'])
    print(r.content)
    # '''

def setInterval(func,time):
    e = threading.Event()
    while not e.wait(time):
        func()

getToken()
setInterval(getTraffic, 2)


