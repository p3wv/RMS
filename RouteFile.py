from main import adresy_url

import requests


class Route:
    def __init__(self, cele, url):
        self.cele = cele
        self.url = url

    def destynacja(self):
        for self.cele in adresy_url:
            self.url = "https://maps.googleapis.com/maps/api/distancematrix/json?origins=Rynek%2057%2C%20G%C5%82og%C3%B3w%2C%20PL%2067-200&destinations={}&units=imperial&departure_time=now&key=AIzaSyD8i4ysTO8mgS2YyuY-O06EVQCty-ld_Pw".format(
                self.cele)

            payload = {}
            headers = {}

            response = requests.request("GET", self.url, headers=headers, data=payload)

            print(response.text)
