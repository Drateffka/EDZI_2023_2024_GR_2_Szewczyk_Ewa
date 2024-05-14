import pandas as pd
import requests
import sqlite3


def get_currency_codes():
    codes = ["USD", "CHF", "EUR", "GBP", "JPY"]
    return codes


def get_data(codes, n):

    results = pd.DataFrame()

    for code in codes:
        url = (
            "https://api.nbp.pl/api/exchangerates/rates/a/"
            + code
            + "/last/"
            + str(n)
            + "/?format=json"
        )
        r = requests.get(url)

        json = r.json()

        df = pd.DataFrame(json["rates"])
        df["currency"] = json["currency"]
        df["code"] = json["code"]

        results = pd.concat([results, df], axis=0)

    return results.reset_index(drop=True)


def connect_database(name):
    con = sqlite3.connect(name)
    cursor = con.cursor()
    return cursor, con


def create_tables(cursor):
    cursor.execute("DROP TABLE IF EXISTS CurrencyInfo")
    cursor.execute("DROP TABLE IF EXISTS CurrencyData")

    cursor.execute(
        """
        CREATE TABLE CurrencyInfo(
            currency_code TEXT PRIMARY KEY, 
            currency_name TEXT
            )
        """
    )
    cursor.execute(
        """CREATE TABLE CurrencyData(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            mid REAL,
            source_table TEXT, 
            effective_date TEXT, 
            currency_code TEXT,
            FOREIGN KEY(currency_code) REFERENCES CurrencyInfo(currency_code)
            )
        """
    )


def load_data(data, cursor, con):
    currencies = data[["currency", "code"]].value_counts().index

    for name, code in currencies:
        cursor.execute("INSERT INTO CurrencyInfo VALUES (?,?)", (code, name))

    for ind, row in data.iterrows():
        cursor.execute(
            "INSERT INTO CurrencyData VALUES (?,?,?,?,?)",
            (ind, row["mid"], row["no"], row["effectiveDate"], row["code"]),
        )

    con.commit()


def main():
    # Get currencies data
    codes = get_currency_codes()
    results = get_data(codes, 25)
    results.to_json("Cwiczenia_6/currency_data.json", orient="records")

    # Save the data to the database
    cur, con = connect_database("Cwiczenia_6/currencies_db.db")
    create_tables(cur)
    load_data(results, cur, con)

    # Close connection to database
    con.close()


if __name__ == "__main__":
    main()
