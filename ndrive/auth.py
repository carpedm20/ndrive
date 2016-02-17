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
        ''' % (keystring, id, password))

    keyname, encpw = str(cx.execute('keyname')), str(cx.execute('encrypted'))

    params = dict(enctp='1',
                  encnm=keyname,
                  svctype='0',
                  enc_url='http0X0.0000000000001P-10220.\
                           0000000.000000www.naver.com',
                  url='www.naver.com',
                  smart_level='1',
                  encpw=encpw)

    session = requests.Session()
    response = session.post('https://nid.naver.com/nidlogin.login', data=params)

    finalize_url = re.search(r'location\.replace\("([^"]+)"\)', response.content).group(1)
    session.get(finalize_url)

    return {
        'NID_AUT': session.cookies.get('NID_AUT'),
        'NID_SES': session.cookies.get('NID_SES')
    }
