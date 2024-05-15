from src.offers import Offer

import requests
from bs4 import BeautifulSoup
from requests.exceptions import InvalidSchema, ConnectionError
from urllib3.exceptions import LocationParseError
import re

ID = 0


class WrongSourceException(Exception):
    pass


class JobOffersCrawler:

    def get_offers_df(self):
        return self.o.df

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

    def scan_offers(self):

        results = []

        for link in self.links:
            bs = self.get_soup(link)

            global ID
            ID = ID + 1

            source = self.source
            position = self.get_position(bs)
            min_wage, max_wage, currency = self.get_wages(bs)
            skills = self.get_skills(bs)
            category = self.category
            seniority = self.get_seniority(bs)
            company = self.get_company(bs)
            results.append(
                [
                    ID,
                    source,
                    position,
                    min_wage,
                    max_wage,
                    currency,
                    skills,
                    category,
                    seniority,
                    link,
                    company,
                ]
            )

            # # DEBUG
            # if ID == 3:
            #     break

        self.o = Offer(results)


class PracujCrawler(JobOffersCrawler):
    url1 = "https://it.pracuj.pl/praca/krakow;wp?rd=0&et=17%2C4%2C18&sal=1&"
    url3 = "its=big-data-science"
    classes = {
        "offer_links": "div.tiles_c1k2agp8 > a.core_n194fgoq",
        "position": "h1",
        "wages": "div.s1n75vtn",
        "currency": ".c1d58j13",
        "skill": "section[data-test='section-technologies-expected']>h3",
        "skill_element": "section[data-test='section-technologies-expected'] li[data-test='item-technologies-expected']",
        "seniority_section": ".offer-viewdZ0-Ni",
        "seniority": ".offer-viewXo2dpV",
        "company": "h2[data-test='text-employerName']",
    }

    source = "pracuj.pl"
    category = "Big Data/Data Science"

    def get_links(self):
        pn = 2
        url = self.url1 + self.url3

        links_all = []

        while 1:
            bs = super().get_soup(url)
            links_bs = bs.select(self.classes["offer_links"])
            links = [link["href"] for link in links_bs]
            links_all = links_all + links

            if len(links) == 0:
                break
            else:
                url = self.url1 + f"pn={pn}&" + self.url3
                pn = pn + 1

        links_all = list(set(links_all))
        self.links = links_all

    def get_position(self, bs):
        pos = bs.select(self.classes["position"])[0].get_text()
        return pos

    def get_wages(self, bs):

        wage_bs = bs.select(self.classes["wages"])[0].get_text()
        multiplier = 168 if "," in wage_bs else 1

        wage_list = wage_bs.split("–")

        min_wage = float(
            float(re.sub("[^0-9, ]", "", wage_list[0]).replace(",", ".")) * multiplier
        )

        if len(wage_list) == 2:
            max_wage = float(
                float(re.sub("[^0-9, ]", "", wage_list[1]).replace(",", "."))
                * multiplier
            )
        else:
            max_wage = min_wage

        currency = bs.select(self.classes["currency"])[0].get_text()

        return min_wage, max_wage, currency

    def get_skills(self, bs):
        skills_text = bs.select(self.classes["skill"])

        skills = []

        if skills_text:
            lis = bs.select(self.classes["skill_element"])

            for li in lis:
                skills.append(li.text)

        return skills

    def get_seniority(self, bs):
        sections = bs.select(self.classes["seniority_section"])

        for s in sections:
            if s["data-scroll-id"] == "position-levels":
                seniorities = (
                    s.select(self.classes["seniority"])[0].get_text().split(", ")
                )
                seniorities_better = []
                for sn in seniorities:
                    if "Junior" in sn:
                        seniorities_better.append("Junior")
                    elif "Mid" in sn:
                        seniorities_better.append("Mid")
                    elif ("Senior" in sn) or ("ekspert" in sn):
                        seniorities_better.append("Senior")
                    else:
                        seniorities_better.append(sn)

                return max(
                    seniorities_better
                )  # Alfabetic order is equal to logical order!

    def get_company(self, bs):
        company = (
            bs.select(self.classes["company"])[0]
            .get_text()
            .replace("O firmie", "")
            .replace("About the company", "")
        )

        return company


class JustJoinCrawler(JobOffersCrawler):
    url = "https://justjoin.it/krakow/data/experience-level_junior.mid.senior/with-salary_yes"
    classes = {
        "offer_links": "a.offer_list_offer_link.css-4lqp8g",
        "position": "h1.css-1u65tlp",
        "wages": ".css-1pavfqb",
        "skill_name": ".MuiTypography-root.MuiTypography-subtitle2.css-x1xnx3",
        "skill_type": ".MuiTypography-root.MuiTypography-subtitle4.css-1wcj8lw",
        "seniority_name": ".css-qyml61",
        "seniority": ".css-15wyzmd",
        "company": ".css-mbkv7r",
    }
    base_url = "https://justjoin.it"
    source = "justjoin.it"
    category = "Data"

    def get_links(self):
        bs = super().get_soup(self.url)
        links_bs = bs.select(self.classes["offer_links"])
        self.links = [self.base_url + link["href"] for link in links_bs]

    def get_position(self, bs):
        pos = bs.select(self.classes["position"])[0].get_text()
        return pos

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

    def get_company(self, bs):
        company = bs.select(self.classes["company"])[0].get_text()

        return company
