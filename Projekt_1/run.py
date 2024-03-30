from src.crawlers import PracujCrawler  # , JustJoinCrawler

# from src.offers import Offer


# 2h 18min
def main():
    pc = PracujCrawler()

    pc.get_links()
    # jjc = JustJoinCrawler()

    # jjc.get_links()

    # jjc.scan_offers()

    # jjc.o.save_json("results/JustJoin.json")

    # df = Offer().read_json("results/JustJoin.json")

    # print(df.head())


if __name__ == "__main__":
    main()
