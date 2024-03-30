from src.offers import Offer

import requests
from bs4 import BeautifulSoup
from requests.exceptions import InvalidSchema, ConnectionError
from urllib3.exceptions import LocationParseError

ID = 0


class WrongSourceException(Exception):
    pass


class JobOffersCrawler:

    def get_offers(self):
        return self.o

    def get_soup(self, url):
        try:
            response = requests.get(url)
        except (InvalidSchema, ConnectionError, LocationParseError) as err:
            print(err)
            return []

        bs = BeautifulSoup(response.text, "html.parser")

        return bs


class PracujCrawler(JobOffersCrawler):
    url = "https://it.pracuj.pl/praca/krakow;wp?rd=0&et=17%2C4%2C18&sal=1&its=big-data-science"
    classes = {"offer_links": ".c1fljezf > a.core_n194fgoq"}

    def get_links(self):
        bs = super().get_soup(self.url)
        links_bs = bs.select(self.classes["offer_links"])
        links = [link["href"] for link in links_bs]
        print(len(links))


class JustJoinCrawler(JobOffersCrawler):
    url = "https://justjoin.it/krakow/data/experience-level_junior.mid.senior/with-salary_yes"
    classes = {
        "offer_links": "a.offer_list_offer_link.css-4lqp8g",
        "wages": ".css-1pavfqb",
        "skill_name": ".MuiTypography-root.MuiTypography-subtitle2.css-x1xnx3",
        "skill_type": ".MuiTypography-root.MuiTypography-subtitle4.css-1wcj8lw",
        "seniority_name": ".css-qyml61",
        "seniority": ".css-15wyzmd",
    }
    base_url = "https://justjoin.it"
    source = "justjoin.it"
    category = "Data"

    def get_links(self):
        bs = super().get_soup(self.url)
        links_bs = bs.select(self.classes["offer_links"])
        self.links = [self.base_url + link["href"] for link in links_bs]

    def get_wages(self, bs):
        wage = bs.select(self.classes["wages"])[0]

        min_wage = int(wage.select("span")[0].string.replace(" ", ""))
        max_wage = int(wage.select("span")[1].string.replace(" ", ""))
        currency = wage.get_text()[-3:]

        return min_wage, max_wage, currency

    def get_skills(self, bs):
        skill_names = bs.select(self.classes["skill_name"])
        skill_types = bs.select(self.classes["skill_type"])

        skills = []

        for s, t in zip(skill_names, skill_types):
            if t.string.upper() != "NICE TO HAVE":
                skills.append(s.string)

        return skills

    def get_seniority(self, bs):
        seniority_name = bs.select(self.classes["seniority_name"])
        seniority = bs.select(self.classes["seniority"])

        for sn, s in zip(seniority_name, seniority):
            if sn.string == "Experience":
                return s.string

    def scan_offers(self):

        results = []

        for link in self.links:
            bs = super().get_soup(link)

            global ID
            ID = ID + 1

            source = self.source
            min_wage, max_wage, currency = self.get_wages(bs)
            skills = self.get_skills(bs)
            category = self.category
            seniority = self.get_seniority(bs)

            results.append(
                [ID, source, min_wage, max_wage, currency, skills, category, seniority]
            )

            # if ID == 3:
            #     break

        self.o = Offer(results)
