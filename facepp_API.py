# -*- coding: utf-8 -*-

import time
import json
import urllib.request
import urllib.error

def connect_to_facepp(filepath):
    '''
    Given the filepath of the image, return a json file
    '''

    http_url = 'https://api-cn.faceplusplus.com/facepp/v3/detect'
    key = "z9XW9np6NcB_wryb27DICAQjq0T_5aUn"
    secret = "tLkQuO2NjH1vKwS3jNUT34aEunV9LkD1"

    boundary = '----------%s' % hex(int(time.time() * 1000))
    data = []
    data.append('--%s' % boundary)
    data.append('Content-Disposition: form-data; name="%s"\r\n' % 'api_key')
    data.append(key)
    data.append('--%s' % boundary)
    data.append('Content-Disposition: form-data; name="%s"\r\n' % 'api_secret')
    data.append(secret)
    data.append('--%s' % boundary)
    fr = open(filepath, 'rb')
    data.append('Content-Disposition: form-data; name="%s"; filename=" "' % 'image_file')
    data.append('Content-Type: %s\r\n' % 'application/octet-stream')
    data.append(fr.read())
    fr.close()
    data.append('--%s' % boundary)
    data.append('Content-Disposition: form-data; name="%s"\r\n' % 'return_landmark')
    data.append('0')
    data.append('--%s' % boundary)
    data.append('Content-Disposition: form-data; name="%s"\r\n' % 'return_attributes')
    data.append(
        "gender,age,smiling,headpose,facequality,blur,eyestatus,emotion,ethnicity,beauty,mouthstatus,eyegaze,skinstatus")
    data.append('--%s--\r\n' % boundary)

    for i, d in enumerate(data):
        if isinstance(d, str):
            data[i] = d.encode('utf-8')

    http_body = b'\r\n'.join(data)
    req = urllib.request.Request(url=http_url, data=http_body)
    req.add_header('Content-Type', 'multipart/form-data; boundary=%s' % boundary)

    try:
        resp = urllib.request.urlopen(req, timeout=5) # post data to server
        qrcont = resp.read() # get response
        facepp = json.loads(qrcont.decode('utf-8'))
        return facepp['faces']
    except urllib.error.HTTPError as e:
        print(e.read().decode('utf-8'))
        return []