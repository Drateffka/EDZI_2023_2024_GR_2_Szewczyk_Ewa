from src.crawlers import PracujCrawler, JustJoinCrawler
from src.offers import Offer
import os


# 5h
def main():
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


if __name__ == "__main__":
    main()
