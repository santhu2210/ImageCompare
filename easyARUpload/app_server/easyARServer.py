import requests
from datetime import datetime, timedelta
from hashlib import sha1, md5
import urllib2, base64, urllib, httplib, json
import base64, os
from django.conf import settings




appKey = '5e4679ed96ac9d5e35f7e792fa78f845' #'9898759662d635aae321ec43af02ea6b' #'97004661a385b0016168a03560f23ed1'  #'910a0420619c0c5a493fee4e420f98db';
appSecret = 'o7dO6f76JHsjpF7aH5f81dAxwnHIynyPeQmhjMrzp5Wg5nEgR5KZKbWx4TPncH8gOnFGQiwq42rraiD7aZQ3YdoUGeafx8MSaCvLbTBucdr1e4jmgrfPjDTDz8Ti4Sxj'#'7OoTXSpt2uPeMj7isN87K5moXFF2s0z5DokmYdYOOSrMuWAhof3h3KIzXr6mjWQH86KgvabUqkRmMkzVREi66H0samfmITdPPI4gLeAsU5fDxyVeLSQPBNKV0f0iQdXJ' #'YArYEIoNgYWn6Oall2taotiR3j8z1jOtgHEiARkjIxyGdPDLTNGGN73u17Zg2ZJfkna3SY5IQbxEPJYXCNlYUxd7mjyEUkR32Z4hKj7COEQLEFZ2ie6YbDkKHlMYBjaL' #'ytLspEqT8KSaP6GjzgqdI21wzeGmgYd4mJNvNFes8JEoBXbsixHcd3i0SKE7EyIr8vn9iVQPaF34XPZNCkClCYJvD16K5qjYh8MKDbh269oNK8b9ODE3z9hnTa4VCMln';
appHost = 'http://95e3bf98f7b37b63d57a0b983ad22ef7.na1.crs.easyar.com:8888'#'http://643212b0cda22fec5b47702fc48eea4d.na1.crs.easyar.com:8888' #'http://6a2396230281393aa579bfe6af669b88.na1.crs.easyar.com:8888' #'http://718027ab6ef61084ebf7a6be4bb938f8.cn1.crs.easyar.com:8888';

def ksort(d):
     return [(k,d[k]) for k in sorted(d.keys())]

def image_to_b64(image_file):
	with open(image_file.path, "rb") as f:
		encoded_string = base64.b64encode(f.read())
		return encoded_string

def getSign(params):
	# print "params --->", params
	params['appKey'] = appKey
	params['date'] = str(datetime.today().isoformat())[:-3]+'Z'   #datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%s.000Z") #'2018-05-14T00:56:12.000Z'  - timedelta(hours=5, minutes=30)
	sort_dict = ksort(params)
	str_pram = ""
	for k,v in sort_dict:
		str_pram = str_pram+k+v

	str_pram = str_pram+appSecret
	# print "str_pramaeter--->",str_pram
	sha_1 = sha1()
	sha_1.update(str_pram) 
	params['signature'] = sha_1.hexdigest()
	return params

def getTargets():
	params = {}	
	#params['last'] = str(1200)
	params['limit'] = str(7)
	params =  getSign(params)
	r = requests.get(appHost+'/targets/', params=params)
	# print r.url , "\n", r.status_code , "\n", r.content
	return r.json()


def addTarget(imgInstance):
	params = {}
	if imgInstance.formData:
		meta = base64.b64encode(imgInstance.formData)
	elif imgInstance.video:
		meta = base64.b64encode(str(imgInstance.video))
	else:
		meta = base64.b64encode(imgInstance.video_URL)

	params['image'] = image_to_b64(imgInstance.image)
	params['active'] = '1'						# default value for easyAR
	params['name'] =  'video_'+imgInstance.title+'_'+imgInstance.category.name
	params['size'] = '150'						# default value for easyAR
	params['meta'] = meta  #base64.b64encode(str(imgInstance.video)) if imgInstance.video else base64.b64encode(imgInstance.video_URL)
	params['type'] = 'ImageTarget'				# default value for easyAR
	print " image name at addTarget ---> ", imgInstance.image
	params =  getSign(params)
	data = json.dumps(params)
	headers = {'Content-Type': 'application/json; charset=utf-8',	'Content-Length': str(len(data))}
	# print "headers -->", headers, "data --->", data
	r = requests.post(appHost+'/targets/',data=data, headers=headers)	
	return r.json() #r.content


def deleteTarget(imgInstance):
	params = {}	
	targetId = imgInstance.targetID  #'0cd4bc53-c5e4-4d20-9b34-82dabab69167'
	params =  getSign(params)
	r = requests.delete(appHost+'/target/'+targetId, params=params)
	# print r.url , "\n", r.status_code , "\n", r.content
	return r.json()


def get_client_ip(request):
	x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
	if x_forwarded_for:
		ip = x_forwarded_for.split(',')[0]
	else:
		ip = request.META.get('REMOTE_ADDR')
	return ip


def current_site_url():
    """Returns fully qualified URL (no trailing slash) for the current site."""
    from django.contrib.sites.models import Site
    current_site = Site.objects.get_current()
    protocol = getattr(settings, 'MY_SITE_PROTOCOL', 'http')
    port     = getattr(settings, 'MY_SITE_PORT', '')
    url = '%s://%s' % (protocol, current_site.domain)
    if port:
        url += ':%s' % port
    return url

def similar_img(imgInstance):
	params = {}
	params['image'] = image_to_b64(imgInstance.image)
	params =  getSign(params)
	data = json.dumps(params)
	headers = {'Content-Type': 'application/json; charset=utf-8',	'Content-Length': str(len(data))}
	# print "headers -->", headers, "data --->", data
	r = requests.post(appHost+'/similar/',data=data, headers=headers)	
	return r.json() #r.content



# GT = getTargets()
# print GT['result']['targets'][0]['targetId']

# AT = addTarget()
# print AT

# DT = deleteTarget()
# print DT