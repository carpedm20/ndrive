"""
This is a snippet based on a post 'http://acuros.pe.kr/?p=198'.

spidermokey is used to log in Naver by using JavaScript.

"""

import os
import re
import requests
import rsa


def nidStringJoin(l):
    return ''.join([chr(len(s)) + s for s in l])


def encrypt(keystring, uid, upw):
    sessionkey, keyname, e_str, n_str = keystring.split(',')
    e, n = int(e_str, 16), int(n_str, 16)

    message = nidStringJoin([sessionkey, uid, upw])

    pubkey = rsa.PublicKey(e, n)
    encrypted = rsa.encrypt(message, pubkey)

    return keyname, encrypted.encode('hex')


def getCookie(id, password):
    keystring = requests.get('http://static.nid.naver.com/enclogin/keys.nhn').content

    keyname, encpw = encrypt(keystring, id, password)

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
