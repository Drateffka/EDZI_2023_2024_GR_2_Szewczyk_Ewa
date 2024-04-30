import requests
import codecs
from summarizer import Summarizer


def get_wikipedia_article_text(article_name="Beaver"):
    # Endpoint URL for the MediaWiki API
    endpoint = "https://en.wikipedia.org/w/api.php"

    article_params = {
        "action": "query",
        "format": "json",
        "prop": "extracts",
        "titles": article_name,  # By deafault article about beavers <3
        "explaintext": True,
    }
    article_response = requests.get(endpoint, params=article_params)
    if article_response.status_code == 200:
        article_data = article_response.json()
        article_text = next(iter(article_data["query"]["pages"].values()))["extract"]
        return article_text
    else:
        print("Failed to fetch article text")


def save_text(text, file_name):
    with codecs.open(f"Cwiczenia_7/{file_name}", "w", "utf-8") as file:
        file.write(text)


def create_summarization(input_text):
    s = Summarizer()
    summary = s(input_text, min_length=50, max_length=150)
    return summary


def main():
    article_text = get_wikipedia_article_text("Beaver")
    save_text(article_text, "org.txt")
    summary = create_summarization(article_text)
    save_text(summary, "outcome.txt")


if __name__ == "__main__":
    main()
