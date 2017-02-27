from top import Auth
import requests
import time

class Search(Auth):

    def get_profile(self, company):
        f = requests.get(self.churl + "company/" + company, auth=(self.key, ""))
        try:
            self.ratelimit(f)
        except KeyError:
            print("Ratelimit Failed")
        data = f.json()
        if "errors" in data:
            return({"company_name":"not_found"})
        else:
            return(data)

    def get_search(self, company):
        f = requests.get(self.churl + "search/companies?q=" + company, auth=(self.key, ""))
        try:
            self.ratelimit(f)
        except KeyError:
            print("Ratelimit Failed")
        data = f.json()
        if "errors" in data:
            return({"company_name":"not_found"})
        else:
            return(data)

    def get_insolvency(self, company):
        f = requests.get(self.churl + "company/" + company + "/insolvency", auth=(self.key, ""))
        try:
            self.ratelimit(f)
        except KeyError:
            print("Ratelimit Failed")
        data = f.json()
        if "errors" in data:
            return({"company_name":"not_found"})
        return(data)


    def has_insolvency(self, company):
        f = requests.get(self.churl + "company/" + company, auth=(self.key, ""))
        try:
            self.ratelimit(f)
        except KeyError:
            print("Ratelimit Failed")
        data = f.json()
        if "errors" in data:
            return({"company_name":"not_found"})
        else:
            return(data.get("has_insolvency_history","NA"))

    def get_postcode(self, company):
        f = requests.get("https://api.companieshouse.gov.uk/company/" + str(company), auth=(self.key, ""))
        try:
            self.ratelimit(f)
        except KeyError:
            print("Ratelimit Failed")
        data = f.json()
        if "errors" in data:
            return ({"company_name":"not_found"})
        if "postal_code" not in data["registered_office_address"]:
            return ("")
        else:
            return(data["registered_office_address"]["postal_code"])


    def ratelimit(self, requests_object, test=False):
        limit = int(requests_object.headers["X-Ratelimit-Remain"])
        if test:
            return limit
        if limit == 0:
            sleep_time = int(requests_object.headers["X-Ratelimit-Reset"]) - time.time()
            print("Waiting " + "{:.0f}".format(sleep_time) + " seconds until ratelimit reset before resuming")
            time.sleep(sleep_time + 1)
        elif limit % 50 == 0:
            print("There are " + str(limit) + " requests remaining before hitting the rate limit")

            
    def upload(self, text_file):
        data = []
        with open(text_file, "r") as file:
            for row in file:
                number = row.rstrip()
                if len(number) == 7:
                    data.append("0" + number)
                elif len(number) == 6:
                    data.append("00" + number)
                else:
                    data.append(number)
        return(data)
