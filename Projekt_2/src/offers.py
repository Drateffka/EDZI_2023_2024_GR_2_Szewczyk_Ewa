import pandas as pd


class Offer:
    colnames = [
        "offer_id",
        "source",
        "position",
        "min_wage",
        "max_wage",
        "currency",
        "skills/technologies",
        "category",
        "seniority",
        "link",
        "company",
    ]

    def __init__(self, data=None):
        self.df = pd.DataFrame(data, columns=self.colnames)

    def append_df(self, new_df):
        self.df = pd.concat([self.df, new_df], ignore_index=True)
        return self.df

    def save_json(self, path):
        self.df.to_json(path, orient="records")

    def read_json(self, path):
        self.df = pd.read_json(path, orient="records")
        return self.df
