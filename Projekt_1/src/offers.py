import pandas as pd


class Offer:
    colnames = [
        "offer_id",
        "source",
        "min_wage",
        "max_wage",
        "currency",
        "skills/technologies",
        "category",
        "seniority",
    ]

    def __init__(self, data=None):
        self.df = pd.DataFrame(data, columns=self.colnames)

    def save_json(self, path):
        self.df.to_json(path, orient="records")

    def read_json(self, path):
        self.df = pd.read_json(path, orient="records")
        return self.df
