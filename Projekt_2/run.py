from src.crawlers import PracujCrawler, JustJoinCrawler
from src.offers import Offer
from src.analisis import (
    skills_counter,
    positions_counter,
    save_results_one_json,
    skills_plotter,
    positions_plotter,
)
from src.database_utils import connect_database, create_tables
import os


def main():

    # ********** Project 1 scope **********

    # Scraping
    # If there is a need to rerun the scraping - delete file
    if not os.path.exists("results/offers.json"):
        pc = PracujCrawler()
        pc.get_links()
        pc.scan_offers()

        jjc = JustJoinCrawler()
        jjc.get_links()
        jjc.scan_offers()

        pc_offers = pc.get_offers()
        jj_offers_df = jjc.get_offers_df()

        df = pc_offers.append_df(jj_offers_df)

        pc_offers.save_json("results/offers.json")
    else:
        df = Offer().read_json("results/offers.json")

    # Analysis
    skills_count = skills_counter(df["skills/technologies"])
    positions_count = positions_counter(df)

    save_results_one_json(skills_count, positions_count)
    skills_plotter(skills_count)
    positions_plotter(positions_count)

    # ********** Project 2 scope **********
    cur, con = connect_database("results/offers_database.db")
    create_tables(cur, con)

    con.close()


if __name__ == "__main__":
    main()
