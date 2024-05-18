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
            name TEXT,
            company_address TEXT
        );"""
    )

    cursor.execute(
        """CREATE TABLE DimPosition(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT
        );"""
    )

    cursor.execute(
        """CREATE TABLE DimSkill(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT
        );"""
    )
    cursor.execute(
        """CREATE TABLE DimCurrency(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT
        );"""
    )
    cursor.execute(
        """CREATE TABLE DimSource(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT
        );"""
    )
    cursor.execute(
        """CREATE TABLE DimCategory(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT
        );"""
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
            description TEXT,
            FOREIGN KEY(id_position) REFERENCES DimPosition(id),
            FOREIGN KEY(id_company) REFERENCES DimCompany(id),
            FOREIGN KEY(id_category) REFERENCES DimCategory(id),
            FOREIGN KEY(id_currency) REFERENCES DimCurrency(id),
            FOREIGN KEY(id_source) REFERENCES DimSource(id)
            );
        """
    )

    con.commit()


def load_data(cursor, con, df):

    tables = ["DimPosition", "DimCurrency", "DimSource", "DimCategory"]
    col_names = ["position", "currency", "source", "category"]

    for _, row in df.iterrows():

        foreign_ids = {}

        # "Simple", repetitive tables
        for col, tab in zip(col_names, tables):
            val = row[col]

            cursor.execute(f"SELECT id FROM {tab} WHERE name = '{val}'")
            result = cursor.fetchone()

            if result is None:
                cursor.execute(f"INSERT INTO {tab} (name) VALUES ('{val}')")
                foreign_ids[col] = cursor.lastrowid
            else:
                foreign_ids[col] = result[0]

        # Company - different situation because we need to fill the address field
        val = row["company"]

        cursor.execute(f"SELECT id FROM DimCompany WHERE name = '{val}'")
        result = cursor.fetchone()

        if result is None:
            if row["company_address"] is not None:
                addr = row["company_address"].replace("'", "")
            else:
                addr = None

            cursor.execute(
                f"INSERT INTO DimCompany (name, company_address) VALUES ('{val}','{addr}')"
            )
            foreign_ids["company"] = cursor.lastrowid
        else:
            foreign_ids["company"] = result[0]

        # Skills - different situation because we have a list of skills
        skills = row["skills/technologies"]
        skills_id_array = []

        for skill in skills:
            cursor.execute(f"SELECT id FROM DimSkill WHERE name = '{skill}'")
            result = cursor.fetchone()

            if result is None:
                cursor.execute(f"INSERT INTO DimSkill (name) VALUES ('{skill}')")
                skills_id_array.append(cursor.lastrowid)
            else:
                skills_id_array.append(result[0])

        # Adding all to fact table
        cursor.execute(
            """INSERT INTO FactOffer (id_position, id_company, id_category, id_currency, id_source,
            link, skills, seniority, wage_min, wage_max, description) VALUES (?,?,?,?,?,?,?,?,?,?,?)""",
            (
                foreign_ids["position"],
                foreign_ids["company"],
                foreign_ids["category"],
                foreign_ids["currency"],
                foreign_ids["source"],
                row["link"],
                str(skills_id_array),
                row["seniority"],
                row["min_wage"],
                row["max_wage"],
                row["description"],
            ),
        )

        con.commit()
