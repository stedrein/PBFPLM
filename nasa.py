import requests
import os
import json


class Celestial:
    def __init__(self, name, description, media):
        self.name: str = name
        self.description: str = description
        self.picture: str = media

    def get_name(self):
        return self.name

    def get_description(self):
        useless_index = self.description.find("APOD in world languages")
        result_description = self.description

        if useless_index != -1:  # Deletes useless info about other languages if such exists
            result_description = self.description[:useless_index]
        return result_description

    def get_picture(self):
        return self.picture


# Returns object of Celestial class from NASA's APOD API
def get_celestial_of_the_day() -> Celestial:
    celestial_response = requests.get("https://api.nasa.gov/planetary/apod" + "?api_key=" + os.environ['NASA_TOKEN'])
    celestial_data = json.loads(celestial_response.text)

    name = celestial_data['title']
    description = celestial_data['explanation']
    picture = celestial_data['url']

    return Celestial(name, description, picture)


def get_random_celestial() -> Celestial:
    celestial_response = requests.get("https://api.nasa.gov/planetary/apod" + "?api_key=" + os.environ['NASA_TOKEN'])
    celestial_data = json.loads(celestial_response.text)

    return None
