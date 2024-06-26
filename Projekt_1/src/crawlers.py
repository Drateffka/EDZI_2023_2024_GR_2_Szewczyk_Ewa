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
                ]
            )

            # DEBUG
            # if ID == 3:
            #     break

        self.o = Offer(results)


class PracujCrawler(JobOffersCrawler):
    url1 = "https://it.pracuj.pl/praca/krakow;wp?rd=0&et=17%2C4%2C18&sal=1&"
    url3 = "its=big-data-science"
    classes = {
        "offer_links": ".c1fljezf > a.core_n194fgoq",
        "position": "h1",
        "wage_min": "span.offer-viewZGJhIB",
        "wage_max": "span.offer-viewYo2KTr",
        "skill": ".offer-viewfjH4z3",
        "skill_element": "p.offer-viewU0gxPf",
        "seniority_section": ".offer-viewdZ0-Ni",
        "seniority": ".offer-viewXo2dpV",
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
        max_wage = bs.select(self.classes["wage_max"])[0].get_text()
        max_wage = re.sub("[^0-9, ]", "", max_wage)
        max_wage = (
            float(float(max_wage.replace(",", ".")) * 168)
            if "," in max_wage
            else float(max_wage)
        )

        min_wage = bs.select(self.classes["wage_min"])

        if len(min_wage) == 0:
            min_wage = max_wage
        else:
            min_wage = re.sub("[^0-9, ]", "", min_wage[0].get_text())
            min_wage = (
                float(float(min_wage.replace(",", ".")) * 168)
                if "," in min_wage
                else float(min_wage)
            )

        return min_wage, max_wage, "zł"

    def get_skills(self, bs):
        skills_text = bs.select(self.classes["skill"])

        skills = []
        for st in skills_text:
            if st["data-test"] == "section-technologies-expected":
                skills_elements = st.select(self.classes["skill_element"])
                for el in skills_elements:
                    skills.append(el.get_text())
                break

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
