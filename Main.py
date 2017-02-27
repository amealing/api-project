#!/bin/env python2.7

import os
import time
import sys
import csv

import logging
import datetime
import pandas as pd

from search import Search
from permitted_users import permitted_users
from email_functions import *

class email_CH_API(Search):

	def __init__(self):

		logging.basicConfig(filename='info.log',level=logging.INFO)
		logging.getLogger("requests").setLevel(logging.WARNING)

		self.input_folder = os.path.join(os.getcwd(),'input')
		self.output_folder = os.path.join(os.getcwd(),'output')

		self.permitted_users = permitted_users

		self.credentials = {"username":os.environ["USERNAME"]
					, "password":os.environ["PASSWORD"]
					}

	def Run(self):
		
		print "Script commencing... checking email every 15 seconds"
		
		while True:
			time.sleep(15)
			try:
				info = check_email_return_attachments(self.credentials["username"], self.credentials["password"], self.input_folder)
			except:
				logging.exception('check_email')
				continue
			if info:
				print info
				email_address = get_email_from_string(info['From'])
				if not is_email_permitted(email_address, self.permitted_users):
					continue
				if not info['attachments']:
					send_email_safely(self.credentials["username"], self.credentials["password"], info["From"]
					,"Your Data Request","No valid CSV or TXT file was detected")
					continue
				# Confirm receipt to sender
				send_email_safely(self.credentials["username"], self.credentials["password"], info["From"]
				,"Your Data Request","Request is being processed")                
				
				send_files = []
				final_email_body = ""
				for file in info['attachments']:
					if self.num_cols_in_file(self.input_folder, file) != 1:
						final_email_body = ''.join([final_email_body,"ERROR: file {0} should contain one column only\n".format(file)])
					else:
						input_file_path = os.path.join(self.input_folder, file)
						output_file_path = self.create_output_file_path(self.output_folder, file)
						try:
							self.data_query(input_file_path,output_file_path) # send query to CH API
							send_files.append(output_file_path)
						except:
							logging.exception('data_query for file {0}'.format(file))
							final_email_body = ''.join([final_email_body,"ERROR: Failed to query data for file {0}\n".format(file)])
				try:
					send_email_safely(self.credentials["username"], self.credentials["password"], info["From"]
						,"Your Data Request", final_email_body, send_files)
				except:
					logging.exception('Sending output files') 
					continue
			else:
				print "no new emails - {}".format(datetime.datetime.today().strftime("%Y-%m-%d at %H:%M:%S")) 


	def data_query(self, input_file_path, output_file_path):

		Inst = Search()
		
		numbers = Inst.upload(input_file_path)
		
		with open(output_file_path, "w+") as csvfile:
			writer = csv.writer(csvfile, lineterminator="\n")
			writer.writerow(["Number", "Company", "Status", "Postcode", "SIC Code", "Insolvency History", 
							 "Insolvency Cases", "Case 1", "Case 1 Dates",
							 "Case 2", "Case 2 Dates", "Case 3", "Case 3 Dates"])
			for number in numbers:
				try:
					data = Inst.get_profile(number)
				except ProxyError:
					logging.exception('data_query for number {0}'.format(number))
					try:
						data = Inst.get_profile(number)
					except ProxyError:
						logging.exception('data_query for number {0}'.format(number))
						writer.writerow([number, "Companies House failed to respond"])
						continue
				if data["company_name"] == "not_found":
					print(number + " not found")
					writer.writerow([number, "not found"])
				else:
					data_w = [number, data["company_name"], data["company_status"],
							  data["registered_office_address"].get("postal_code","na"), data.get("sic_codes","-")[0]]
					has_insol = Inst.has_insolvency(number)
					data_w.append(str(has_insol))
					if has_insol == True:
						cases = Inst.get_insolvency(number)
						data_w.append(str(len(cases["cases"])))
						for case in cases["cases"]:
							data_w.append(case["type"])
							data_w.append(case["dates"])
					print(data_w)
					writer.writerow(data_w)

		print("Query completed")

	def create_output_file_path(self, target_dir, csv_text_file):
		output_file = csv_text_file.split('.')[0] + '_output.csv'
		output_file_path = os.path.join(target_dir, output_file)
		return output_file_path

	def num_cols_in_file(self, target_dir, csv_text_file):
		with open(os.path.join(target_dir, csv_text_file), 'r') as file:
			pd_file = pd.read_csv(file, header=None)
			num_cols = len(pd_file.columns)
			return num_cols

if __name__ == "__main__":
	inst = email_CH_API()
	inst.Run()
