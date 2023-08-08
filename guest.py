import time
import requests


if __name__ == '__main__':
	while 1 :
		print('send the request!')
		url = 'http://111.230.56.222:8000/home'
		p = {"key":"asdasdasdasdasdasd",
			"date":"2014-09-11"}
		headers = { 'Connection': 'close'};
		a = requests.get(url)
		print("request_code : " + str(a.status_code))
		print(a.text)
		print(a.cookies)
		time.sleep(0.5)
