

import os
import requests
import urllib, re
from jsbn import RSAKey


def getLenChar(texts):
    texts = texts + ''
    return chr(len(texts))


def getCookie(id, password):
    f = urllib.urlopen('http://static.nid.naver.com/enclogin/keys.nhn')

    keystring = f.read()
    f.close()

    rsa = RSAKey()
    keys =  keystring.split(",")
    sessionkey = keys[0]
    keyname = keys[1]
    evalue = keys[2]
    nvalue = keys[3]
    rsa.setPublic(evalue,nvalue)
    encpw = rsa.encrypt(getLenChar(sessionkey)+sessionkey+getLenChar(id)+id+getLenChar(password)+password)


    params = dict(enctp='1',
                  encnm=keyname,
                  svctype='0',
                  enc_url='http0X0.0000000000001P-10220.\
                           0000000.000000www.naver.com',
                  url='www.naver.com',
                  smart_level='1',
                  encpw=encpw)


    params = urllib.urlencode(params)

    headers = {'Content-type': 'application/x-www-form-urlencoded',
               'Accept':'text/plain'}

    session = requests.session()


    response = session.post('https://nid.naver.com/nidlogin.login', params=params, headers=headers)
    data = response.text


    headers = {'Accept':'text/plain'}
    if response.status_code == 302:
        location = response.getheader('location')
        url = re.match(r'https:\/\/[\w+\.]*.*', location).group()

    elif response.status_code == 200:
        url = re.search(r'https:\/\/?[\w+\.]*.*', data).group()

    session.get(url,headers=headers)
    return session.cookies.get_dict()

