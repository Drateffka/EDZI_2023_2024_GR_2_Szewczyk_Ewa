import sqlite3


def connect_database(name):
    con = sqlite3.connect(name)
    cursor = con.cursor()
    return cursor, con


def create_tables(cursor, con):
    cursor.execute("DROP TABLE IF EXISTS FactOffer")
    cursor.execute("DROP TABLE IF EXISTS DimCompany")
    cursor.execute("DROP TABLE IF EXISTS DimPosition")
    cursor.execute("DROP TABLE IF EXISTS DimSkill")
    cursor.execute("DROP TABLE IF EXISTS DimCurrency")
    cursor.execute("DROP TABLE IF EXISTS DimSource")
    cursor.execute("DROP TABLE IF EXISTS DimCategory")

    cursor.execute(
        """
            CREATE TABLE DimCompany(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            company_name TEXT
        );"""
    )

    cursor.execute(
        """CREATE TABLE DimPosition(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            position_name TEXT
        );"""
    )

    cursor.execute(
        """CREATE TABLE DimSkill(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            skill_name TEXT
        );"""
    )
    cursor.execute(
        """CREATE TABLE DimCurrency(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            currency_name TEXT
        );"""
    )
    cursor.execute(
        """CREATE TABLE DimSource(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            source_name TEXT
        );"""
    )
    cursor.execute(
        """CREATE TABLE DimCategory(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            category_name TEXT
        );"""
    )
    cursor.execute(
        "INSERT INTO DimSource (source_name) VALUES ('pracuj.pl'), ('justjoin.it')"
    )

    cursor.execute(
        "INSERT INTO DimCategory (category_name) VALUES ('Big Data/Data Science'), ('Data')"
    )

    cursor.execute(
        """
        CREATE TABLE FactOffer(
            id_offer INTEGER PRIMARY KEY AUTOINCREMENT,
            id_position INTEGER,
            id_company INTEGER,
            id_category INTEGER,
            id_currency INTEGER,
            id_source INTEGER,
            link TEXT,
            skills TEXT,
            seniority TEXT,
            wage_min REAL,
            wage_max REAL,
            FOREIGN KEY(id_position) REFERENCES DimPosition(id),
            FOREIGN KEY(id_company) REFERENCES DimCompany(id),
            FOREIGN KEY(id_category) REFERENCES DimCategory(id),
            FOREIGN KEY(id_currency) REFERENCES DimCurrency(id),
            FOREIGN KEY(id_source) REFERENCES DimSource(id)
            );
        """
    )

    con.commit()


def load_data(df):
    print(df.head())
