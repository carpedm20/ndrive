"""
This is a snippet based on a post 'http://acuros.pe.kr/?p=198'.

spidermokey is used to log in Naver by using JavaScript.

"""

import os
import requests
import urllib, base64, rsa, httplib, re
import spidermonkey

def getCookie(id, password):
    f = urllib.urlopen('http://static.nid.naver.com/enclogin/keys.nhn')

    keystring = f.read()
    f.close()

    # login JavaScript from 'https://nid.naver.com/login/js/login.long.js'
    js_path = os.path.join(os.path.dirname(__file__), 'login.long.js')
    f = file(js_path, 'r')
    js = f.read()
    f.close()

    rt = spidermonkey.Runtime()
    cx = rt.new_context()
    cx.execute(js)
    cx.execute('''
        keystr = '%s';
        rsa = new RSAKey();
        keySplit();
        rsa.setPublic(evalue, nvalue);
        uid = '%s';
        upw = '%s';
        encrypted = rsa.encrypt(getLenChar(sessionkey)+sessionkey\
                    +getLenChar(uid)+uid+getLenChar(upw)+upw);
        ''' %(keystring, id, password))

    keyname, encpw = str(cx.execute('keyname')), str(cx.execute('encrypted'))
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
    conn = httplib.HTTPSConnection('nid.naver.com')
    conn.request('POST', '/nidlogin.login', params, headers)
    response = conn.getresponse()
    data = response.read()
    conn.close()
    cookie = response.getheader('set-cookie')

    while True:
        headers = {'Accept':'text/plain', 'Cookie':cookie}
        if response.status == 302:
            location = response.getheader('location')
            host, url = re.match(r'http:\/\/([\w+\.]*)(.*)', location).groups()
        elif response.status == 200:
            host, url = re.search(r'"(?:http:\/\/)?([\w+\.]*)(.*)"', data).groups()
        conn = httplib.HTTPConnection(host)
        conn.request('GET', url, '', headers)
        response = conn.getresponse()
        data = response.read()
        if response.status == 302:
            cookie = response.getheader('set-cookie').replace(';, ', '; ')
        conn.close()
        if host == 'www.naver.com':
            break

    cookies = [c.split('=',1) for c in cookie.split(';')]

    cookie = {}
    for c in cookies:
        try:
            key = c[0].strip()
            value = c[1].strip()

            cookie[key] = value
        except:
            continue # do nothing

    return cookie
