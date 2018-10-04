import logging
import urllib2, base64, urllib, httplib
from wsgiref.handlers import format_date_time
from datetime import datetime
from time import mktime
from urlparse import urlparse
from hashlib import sha1, md5
from hmac import new as hmac
import json
import requests



class Vuforia:
    def __init__(self, access_key, secret_key, host="https://vws.vuforia.com"):
        self.access_key = access_key
        self.secret_key = secret_key
        self.host = host

    def _get_rfc1123_date(self):
        now = datetime.now()
        stamp = mktime(now.timetuple())
        return format_date_time(stamp)

    def _get_request_path(self, req):
        o = urlparse(req.get_full_url())
        return o.path

    def _hmac_sha1_base64(self, key, message):
        return base64.b64encode(hmac(key, message, sha1).digest())

    def _get_content_md5(self, req):
        if req.get_data():
            return md5(str(req.get_data())).hexdigest()
        return "d41d8cd98f00b204e9800998ecf8427e"

    def _get_content_type(self, req):
        if req.get_method() == "POST":
            print "inside post _ get req"
            return "application/json"
        return ""

    def _get_authenticated_response(self, req):
        rfc1123_date = self._get_rfc1123_date()
        string_to_sign =\
            req.get_method() + "\n" +\
            self._get_content_md5(req) + "\n" +\
            self._get_content_type(req) + "\n" +\
            rfc1123_date + "\n" +\
            self._get_request_path(req)
        print "string to sign --->" , string_to_sign
        signature = self._hmac_sha1_base64(self.secret_key, string_to_sign)

        req.add_header('Date', rfc1123_date)
        auth_header = 'VWS %s:%s' % (self.access_key, signature)
        req.add_header('Authorization', auth_header)
        # TODO: Add handelr for error codes like 403 "TargetNameExist"
        rspns = urllib2.urlopen(req)
        print "response ---->",rspns
        return rspns

    def get_target_by_id(self, target_id):
        url = '%s/targets/%s' % (self.host, target_id)
        req = urllib2.Request(url)
        response = self._get_authenticated_response(req)
        return json.loads(response.read())['target_record']

    def get_target_ids(self):
        url = '%s/targets' % self.host
        req = urllib2.Request(url)
        response = self._get_authenticated_response(req)
        return json.loads(response.read())['results']

    def get_summary(self):
        url = '%s/summary' % self.host
        req = urllib2.Request(url)
        response = self._get_authenticated_response(req)
        return json.loads(response.read())

    def get_targets(self):
        targets = []
        for target_id in self.get_target_ids():
            targets.append(self.get_target_by_id(target_id))
        return targets


    # results = requests.get("http://www.bing.com/search", 
    #           params={'q': query, 'first': page}, 
    #           headers={'User-Agent': user_agent})

    def _get_auth_header(self, req):
        rfc1123_date = self._get_rfc1123_date()
        string_to_sign =\
            req.get_method() + "\n" +\
            self._get_content_md5(req) + "\n" +\
            self._get_content_type(req) + "\n" +\
            rfc1123_date + "\n" +\
            self._get_request_path(req)
        print "string to sign --->" , string_to_sign
        signature = self._hmac_sha1_base64(self.secret_key, string_to_sign)

        auth_header = 'VWS %s:%s' % (self.access_key, signature)
        return auth_header


    def add_target(self, data):
        url = '%s/targets' % self.host
        print "url -->", url
        data = json.dumps(data)
        req = urllib2.Request(url, data, {'Content-Type': 'application/json'})
        # sending post request and saving response as response object
        #req = requests.post(url = url, data = data ,headers = {'content-type': 'application/json'})
        auth_header = self._get_auth_header(req)
        date = self._get_rfc1123_date()

        request_headers = {
        #'Accept': 'application/json',
        'Authorization': auth_header,
        'Content-Type': 'application/json',
        'Date': date
        }
        print "request header ---->", request_headers

        # Make the request over HTTPS on port 443
        http = httplib.HTTPSConnection('vws.vuforia.com', 443)
        http.request('POST', '/targets', data, request_headers)

        response = http.getresponse()
        response_body = response.read()


        print "response_body --->", response_body
        # response = self._get_authenticated_response(req)
        return json.loads(response.read())

def main():
    v = Vuforia(access_key="cc23b4affa340e0c35b66974c9b14513c5c3a354",
                secret_key="70e14e813fe7232537e0d50af6d30e502ce18594")
    # for target in v.get_targets():
    #     print target

    # print v.get_summary()

    image_file = open('logo.png')
    image = base64.b64encode(image_file.read())
    metadata_file = open('license.txt')
    metadata = base64.b64encode(metadata_file.read())
    # print "image --->" , image ,"\n","metadata ---->", metadata
    print v.add_target({"name": "zxczxc", "width": "320.0", "image": image, "application_metadata": metadata, "active_flag": 1})

if __name__ == "__main__":
    main()
