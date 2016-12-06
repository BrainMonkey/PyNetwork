#from __future__ import print_function
import requests, re, json, urllib

user = 'nsroot'
password = 'password'
netscaler = 'X.X.X.X'


#LOGIN
url = 'http://%s/nitro/v1/config/' % netscaler
response = requests.get(url, auth=(user, password), verify=False)
data = response.json()

#GET JSON
stat_url_test = 'http://%s/nitro/v1/config/sslcertkey' % (netscaler)
response2 = requests.request("GET",stat_url_test, auth=(user, password))
json_output = response2.text
json_parsed = json.dumps(json.loads(json_output))



response_json = json_parsed.replace("'", '"')
response_json = json.loads(response_json)
for doc in response_json['sslcertkey']:
	expire = unicode(doc['daystoexpiration'])
	cert = unicode(doc['cert'])
	
	#print ("Certificate: " + cert + "\nExpires in " + expire + " days." + "\n")

	
	if str(expire).split() <= '30':
		print "CERT: " + cert + "\nExpires in " + expire + " days." + "\n"
    #print(doc['cert'], doc['daystoexpiration'])


#json_output = response2.text
#json_parsed = json.dumps(json.loads(json_output)) #string
#json_parsed2 = json.loads(json_output) #dict


#<WORKS
#response3 = requests.get(stat_url_test, auth=(user, password))
#x = response3.json()
#print x['sslcertkey'][0]['certkey']
#print x['sslcertkey'][0]['daystoexpiration']
#WORKS>


