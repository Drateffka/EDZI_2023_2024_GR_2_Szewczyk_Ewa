import requests
from bs4 import BeautifulSoup
import string
import pandas as pd


def get_text(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    # mw-parser-output to klasa HTML uzywana na platformie MediaWiki - jest glownym kontenerem dla tresci
    content = soup.find("div", class_="mw-parser-output").text
    return content


def process_text(text):
    text = text.lower()
    translator = str.maketrans(
        "",
        "",
        string.punctuation
        + "\n"
        + "\xa0"
        + "0123456789",  # usuwamy interpunkcje, nowe linie, cyfry
    )  # źródło: https://blog.enterprisedna.co/python-remove-punctuation-from-string/#:~:text=To%20remove%20punctuation%20from%20a,new%20string%20excluding%20punctuation%20marks.
    text = text.translate(translator)
    return text


def get_ranked_words(text):
    words_list = pd.Series(text.split(" "))  # stworzenie serii danych
    words_list = words_list[words_list != ""]  # usunięcie pustych słów
    ranked_words = words_list.value_counts()[
        :100
    ]  # zliczenie i wybranie pierwszych 100
    ranked_words = ranked_words.reset_index()
    ranked_words.columns = ["word", "count"]
    return ranked_words


def write_results(results, filename):
    with open(filename, "w") as file:
        file.write("ranking;slowo;ilosc wystapien\n")  # nagłówek
        for i in range(len(results)):
            word, count = results.loc[i]
            file.write(f"{i+1};{word};{count}\n")  # poszczególne linie


def main():
    url = "https://en.wikipedia.org/wiki/Web_scraping"
    text = get_text(url)
    cleaned_text = process_text(text)
    final_words = get_ranked_words(cleaned_text)
    write_results(final_words, "output.txt")


if __name__ == "__main__":
    main()
