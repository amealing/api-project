#!/bin/env python2.7

import pytest
import requests
import os
from Scripts import search

inst = search.Search()

@pytest.fixture
def company():
    test_comp = {"Name":"UNIVERSAL LEISURE MEDIA LIMITED","Number":"06725465"}
    return test_comp

@pytest.fixture
def test_file():
    return os.path.join(os.getcwd(),"test_file_1.csv")

def test_get_profile(company):
    data = inst.get_profile(company["Number"])
    assert data["company_name"] == company["Name"]

def test_get_search(company):
    data = inst.get_search(company["Name"])
    assert data["total_results"] > 0

def test_get_insolvency(company):
    data = inst.get_insolvency(company["Number"])
    assert data["cases"]

def test_has_insolvency(company):
    data = inst.has_insolvency(company["Number"])
    assert data == True

def test_get_postcode(company):
    data = inst.get_postcode(company["Number"])
    assert data == "MK9 2EA"

def test_ratelimit(company):
    f = requests.get(inst.churl + "company/" + company["Number"], auth=(inst.key, ""))
    result = inst.ratelimit(f, test=True)
    assert isinstance(result, int)

def test_upload(test_file):
    data = inst.upload(test_file)
    assert len(data) == 10
    