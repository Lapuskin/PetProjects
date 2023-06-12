import json

class DataBase:
    def __init__(self):
        self.history = []
        self.deserialize_history()

    def serialize_history(self):
        with open("sources/data/history.json", "w") as fh:
            json.dump(self.history, fh)
    def deserialize_history(self):
        with open("sources/data/history.json", "r") as fh:
            self.history = json.load(fh)

    def upload_history(self, link):
        self.history.append(link)
        self.serialize_history()

    def get_history(self):
        self.deserialize_history()
        return self.history