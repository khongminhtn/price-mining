import os
import csv
import requests
from datetime import datetime
from util import tprint




class IG():
	def __init__(self, endpoint, user, password, key):
		self.headers = {
			"Content-Type": "application/json; charset=UTF-8",
			"Accept": "application/json; charset=UTF-8",
			"VERSION": "1",
			"X-IG-API-KEY": key
		}
		self.session = None
		self.control = None
		self.stream = None
		self.account_id = None
		self.stream_endpoint = None
		self.auth = {
			"endpoint": endpoint + 'session',
			"user": user,
			"password": password
		}


	def authenticate(self):
		# get credentials
		endpoint = self.auth['endpoint']
		payload = {
			"identifier": self.auth['user'],
			"password": self.auth['password']
		}
		# authenticate reqest
		res = requests.post(endpoint, headers=self.headers, json=payload)
		data = res.json()
		status = res.status_code
		tprint(f'Auth: {status}')

		# get tokens
		self.headers['CST'] = res.headers['CST']
		self.headers['X-SECURITY-TOKEN'] = res.headers['X-SECURITY-TOKEN']
		self.account_id = data['currentAccountId']
		self.stream_endpoint = data['lightstreamerEndpoint']


	def get_stream(self):
		# build stream payload
		endpoint = self.stream_endpoint + '/lightstreamer/create_session.txt'
		payload = {
			"LS_op2": "create",
			"LS_cid": "mgQkwtwdysogQz2BJ4Ji kOj2Bg",
			"LS_user": self.account_id,
			"LS_password": f"CST-{self.headers['CST']}|XST-{self.headers['X-SECURITY-TOKEN']}",
			"LS_report_info": "true"
  	}
		# request for stream object
		res = requests.post(endpoint, params=payload, stream=True)
		status = res.status_code
		tprint(f'Stream: {status}')

		# get stream object
		self.stream = res.iter_lines(chunk_size=80, decode_unicode=True)

		# get stream token for further subscription
		for line in self.stream:
			if ':' in line:
				key, value = line.split(':', 1)
				if key == 'SessionId':
					self.session = value
				if key == 'ControlAddress':
					self.control = value
				if self.control and self.session:
					break

		# extract stream tokens to csv
		with open('tokens.csv', 'w', newline='') as file:
			writer = csv.writer(file, delimiter='|')
			writer.writerow([self.session])
			writer.writerow([self.control])



session = IG(
	endpoint=os.environ['DEMO_URL'],
	user=os.environ['DEMO_USER'],
	password=os.environ['DEMO_PASS'],
	key=os.environ['DEMO_KEY']
)