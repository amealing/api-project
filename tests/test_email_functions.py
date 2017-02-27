#!/bin/env python2.7

from Scripts import email_functions as ef
import pytest
import os
import imaplib
import email

## from Main.py
# test create_output_file_path
# test num_cols_in_file

@pytest.fixture
def user():
	return os.environ["USERNAME"]

@pytest.fixture
def password():
	return os.environ["PASSWORD"]

@pytest.fixture
def user_email():
	return os.environ["USERNAME"] + "@gmail.com"

@pytest.fixture
def test_input_folder():
	return os.path.join(os.getcwd(),"input")

@pytest.fixture
def test_file_1():
	return os.path.join(os.getcwd(),"test_file_1.csv")

@pytest.fixture
def test_file_2():
	return os.path.join(os.getcwd(),"test_file_2.csv")

@pytest.fixture
def txt_file():
	return "file.txt"

@pytest.fixture
def email_in_string():
	return "test email <test@gmail.com>"

@pytest.fixture
def safe_subject_test():
	return "SAFE_SUBJECT_TEST"

@pytest.fixture
def wrong_password():
	return "342JG2jl3jl"

def test_send_email(user, password, user_email):

	ef.send_email(user, password, user_email, "TEST_SEND_EMAIL")
	m = ef.check_email(user, password, "TEST_SEND_EMAIL")
	ef.delete_email(user, password, "TEST_SEND_EMAIL")
	assert [user_email,"TEST_SEND_EMAIL"] == m

def test_one_attachment_path(user, password, user_email, test_input_folder, test_file_1):

	ef.send_email(user, password, user_email, "TEST_GET_ONE_ATTACHMENT", files=[test_file_1])
	results = ef.check_email_return_attachments(user, password, test_input_folder)
	ef.delete_email(user, password, "TEST_GET_ONE_ATTACHMENT")
	assert os.path.exists(os.path.join(test_input_folder, test_file_1))
	os.remove(os.path.join(test_input_folder, os.path.basename(test_file_1)))

def test_one_attachment_output(user, password, user_email, test_input_folder, test_file_1):
	
	ef.send_email(user, password, user_email, "TEST_GET_ONE_ATTACHMENT", files=[test_file_1])
	results = ef.check_email_return_attachments(user, password, test_input_folder)
	ef.delete_email(user, password, "TEST_GET_ONE_ATTACHMENT")
	assert [user_email, [os.path.basename(test_file_1)]] == [results['From'],results['attachments']]
	os.remove(os.path.join(test_input_folder, os.path.basename(test_file_1)))

def test_delete_email(user, password, user_email):

	ef.send_email(user, password, user_email, "TEST_DELETE_EMAIL")
	deleted_email_data = ef.delete_email(user, password, "TEST_DELETE_EMAIL")
	assert deleted_email_data == ''

def test_is_txt_csv(txt_file):
	assert ef.is_txt_csv(txt_file)

def test_get_email_from_string(email_in_string):
	assert "test@gmail.com" == ef.get_email_from_string(email_in_string)

def test_send_email_safely(user, wrong_password, user_email, safe_subject_test):
	max_tries = ef.send_email_safely(user, wrong_password, user_email, safe_subject_test)
	assert max_tries == 4

if __name__ == '__main__':
	test_one_attachment_output(os.environ["USERNAME"]
							, os.environ["PASSWORD"]
							, os.environ["USERNAME"] + "@gmail.com"
							, os.path.join(os.getcwd(),"tests","input")
							, os.path.join(os.getcwd(),"tests","test_file_1.csv"))