import os

class Auth(object):

	def __init__(self):
		self.key = os.environ["KEY"]
		self.churl = 'https://api.companieshouse.gov.uk/'

