import pandas as pd


def get_voi_capitals() -> list:
    cities = [
        "Białystok",
        "Gdańsk",
        "Katowice",
        "Kraków",
        "Kielce",
        "Lublin",
        "Łódź",
        "Olsztyn",
        "Opole",
        "Poznań",
        "Rzeszów",
        "Szczecin",
        "Toruń",
        "Warszawa",
        "Wrocław",
        "Zielona Góra",
    ]

    return cities


def get_date(df: pd.DataFrame):
    date_hour = (
        str(df.data_pomiaru.unique()[0])
        + "_"
        + str(df.godzina_pomiaru.unique()[0])
        + ".00"
    )

    return date_hour


def read_data(link: str) -> pd.DataFrame:
    df = pd.read_json(link).set_index("id_stacji")
    df.to_csv(f"Cwiczenia_5/data/{get_date(df)}.csv")
    voi_cities = get_voi_capitals()
    df = df[df.stacja.isin(voi_cities)]

    return df


def get_statistics(df: pd.DataFrame) -> dict:
    cols = ["temperatura", "suma_opadu", "cisnienie"]
    res = dict()

    for col in cols:
        res[col] = {
            "mean": round(df[col].mean(), 2),
            "min": [
                df[df[col] == df[col].min()]["stacja"].values[0],
                round(df[col].min(), 2),
            ],
            "max": [
                df[df[col] == df[col].max()]["stacja"].values[0],
                round(df[col].max(), 2),
            ],
        }

    res["date_hour"] = get_date(df)

    return res


def print_statistics(res: dict):
    for k, v in res.items():
        print("----------", k, "----------", sep="\n")
        if type(v) is dict:
            for kk, vv in v.items():
                print(f"{kk}: {vv}")
        else:
            print(v)


def main():
    df = read_data("https://danepubliczne.imgw.pl/api/data/synop")
    res = get_statistics(df)
    print_statistics(res)


if __name__ == "__main__":
    main()
