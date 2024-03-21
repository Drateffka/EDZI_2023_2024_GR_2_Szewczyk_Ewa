import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
from requests.exceptions import InvalidSchema, ConnectionError
from urllib3.exceptions import LocationParseError
from urllib.robotparser import RobotFileParser
from unidecode import unidecode


def check_robots_txt(url: str) -> RobotFileParser:
    """Function for setting Robot File Parser"""

    rp = RobotFileParser()
    rp.set_url(url)
    rp.read()

    return rp


def get_soup(url: str, robot_parser: RobotFileParser) -> BeautifulSoup:
    """Given url and Robot File Parser checks whether site is available for scrapping and returns soup"""

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
        "Accept-Language": "en-US,en;q=0.9",
    }

    if robot_parser.can_fetch("FilmBot", url):
        print("Scraping allowed")
    else:
        print("Scraping not allowed")
        # return BeautifulSoup()

    try:
        response = requests.get(url, headers=headers)
    except InvalidSchema as err:
        print(f"Invalid schema: {err}")
        return []
    except ConnectionError as err:
        print(f"Connection error: {err}")
        return []
    except LocationParseError as err:
        print(f"Location Parse error: {err}")
        return []

    bs = BeautifulSoup(response.text, "html.parser")

    return bs


def trim_title(string: str) -> str:
    """Trimming IMDB titles (deleting number, dot and whitespace)"""

    return re.sub(r"\d+\.\s*", "", string)


def save_results(
    title_list: list[str], rating_list: list[str], n_links: int
) -> pd.DataFrame:
    """Creating pandas dataframe from titles and ratings list, setting ranking index"""

    results = pd.DataFrame(
        {"Title": title_list, "Rating": rating_list},
        index=pd.Index(list(range(1, n_links + 1))),
    )
    results.index.name = "Ranking"

    return results


def get_imdb_ranking(
    url: str, robot_parser: RobotFileParser, n_links: int = 100
) -> pd.DataFrame:
    """Getting films from imdb ranking"""

    bs = get_soup(url, robot_parser)

    main_class = "div.sc-b0691f29-0.jbYPfh.cli-children"
    title_class = ".ipc-title__text"
    rating_class = ".ipc-rating-star.ipc-rating-star--base.ipc-rating-star--imdb.ratingGroup--imdb-rating"

    films_list = bs.select(main_class)

    title_list = []
    rating_list = []

    for i in range(n_links):
        film = films_list[i]

        title = trim_title(film.select(title_class)[0].get_text())
        rating = float(film.select(rating_class)[0].get_text().split()[0])

        title_list.append(title)
        rating_list.append(rating)

    imdb_results = save_results(title_list, rating_list, n_links)

    return imdb_results


def get_rotten_ranking(
    base_url: str, robot_parser: RobotFileParser, previous_df: pd.DataFrame
) -> pd.DataFrame:
    """Getting films' ratings from Rotten Tomatoes given titles from imdb"""

    search_links = base_url + previous_df.Title.str.replace(" ", "%20")

    title_list = []
    rating_list = []

    for link, imdb_title in zip(search_links, previous_df.Title):
        bs = get_soup(link, robot_parser)

        imdb_title = unidecode(imdb_title.replace(",", "").replace("-", ""))

        candidate_films = bs.select("search-page-media-row")

        for i in range(len(candidate_films)):
            film_text = candidate_films[i]
            title = unidecode(
                film_text.get_text().strip().replace(",", "").replace("-", "")
            )

            if title == imdb_title:
                try:
                    score = int(film_text["tomatometerscore"])
                except ValueError:
                    score = -1

                title_list.append(title)
                rating_list.append(score)

                break

            if i + 1 == len(candidate_films):
                print("No such film on rotten tomatoes!")

    results = save_results(title_list, rating_list, len(title_list))

    return results


def combine_save(imdb: pd.DataFrame, rt: pd.DataFrame) -> pd.DataFrame:
    """Merging ratings from imdb and rotten tomatoes & some minor style fixes"""

    imdb = imdb.reset_index()

    merged = imdb.merge(rt, "left", on="Title", suffixes=["_imdb", "_rt"])

    merged = merged.rename(
        {
            "Title": "tytul_filmu",
            "Ranking": "ranking_imdb",
            "Rating_imdb": "ocena_imdb",
            "Rating_rt": "ocena_rotten_tomatoes",
        },
        axis=1,
    )

    merged = merged[
        ["tytul_filmu", "ranking_imdb", "ocena_imdb", "ocena_rotten_tomatoes"]
    ]

    merged.to_json("Cwiczenia_3/final_results.json", orient="records")


def main():
    """Main function"""

    # For faster testing
    # imdb = pd.read_csv("Cwiczenia_3/imdb.csv", index_col="Ranking")
    # rt = pd.read_csv("Cwiczenia_3/rotten.csv", index_col="Ranking")

    robot_imdb = check_robots_txt("https://www.imdb.com/robots.txt")
    robot_rt = check_robots_txt("https://www.rottentomatoes.com/robots.txt")

    print("Beginning IMDB...")
    imdb = get_imdb_ranking("https://www.imdb.com/chart/top/", robot_imdb, 100)
    print(f"IMDB finished with {len(imdb)} records!")

    print("Beginning Rotten Tomatoes...")
    rt = get_rotten_ranking(
        "https://www.rottentomatoes.com/search?search=", robot_rt, imdb
    )
    print(f"Rotten Tomatoes finished with {len(rt)} records!")
    print(
        "(there might be less records than imdb because of no votes or difficulties finding the film)"
    )

    print("Beginning merging both rankings...")
    combine_save(imdb, rt)
    print("Finished!")


if __name__ == "__main__":
    main()
