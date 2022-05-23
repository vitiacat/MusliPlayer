import json
from os import path


class SettingsError(Exception):

    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message


class Settings:

    def __init__(self):
        self.volume = 100
        self.bookmarks = []

    def load(self):
        if not path.exists('settings.json'):
            self.save()
        else:
            with open('settings.json', 'r') as json_file:
                try:
                    settings = json.load(json_file)
                    self.volume = settings['volume']
                    self.bookmarks = settings['bookmarks']
                except json.decoder.JSONDecodeError:
                    print('Error: settings.json is not valid JSON')
                    raise SettingsError('Parsing error! settings.json is not valid JSON')

    def save(self):
        with open('settings.json', 'w') as json_file:
            json.dump({
                'volume': self.volume,
                'bookmarks': self.bookmarks
            }, json_file)