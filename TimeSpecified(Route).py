import tables

import requests

import RouteFile


class TimeSpecified(RouteFile.Route):
    def __init__(self, cele, url, selected_time):
        RouteFile.Route.__init__(self, cele, url)
        self.selected_time = selected_time

    def destynacja(self):
        for self.cele in tables.adresy_url:
            self.url = "https://maps.googleapis.com/maps/api/distancematrix/json?origins=Rynek%2057%2C%20G%C5%82og%C3%B3w%2C%20PL%2067-200&destinations={}&units=imperial&departure_time={}&key=AIzaSyD8i4ysTO8mgS2YyuY-O06EVQCty-ld_Pw".format(
                self.cele, self.selected_time)

            payload = {}
            headers = {}

            response = requests.request("GET", self.url, headers=headers, data=payload)

            print(response.text)
