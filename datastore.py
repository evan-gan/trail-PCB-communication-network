import ujson as json
import os


class DataStore:
    def __init__(self, db):
        self.db = db
        self.data = {}
        self.load()

    def load(self):
        if os.path.exists(self.db):
            with open(self.db, 'r') as f:
                try:
                    self.data = json.load(f)
                except ValueError:
                    self.data = {}

    def save(self):
        with open(self.db, 'w') as f:
            json.dump(self.data, f)

    def add(self, key, value):
        self.data[key] = value
        self.save()

    def remove(self, key):
        if key in self.data:
            del self.data[key]
            self.save()

    def get(self, key, default=None):
        return self.data.get(key, default)

    def get_all(self):
        return self.data

    def clear(self):
        self.data = {}
        self.save()
