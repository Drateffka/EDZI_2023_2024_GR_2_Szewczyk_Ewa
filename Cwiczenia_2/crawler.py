import requests
from requests.exceptions import InvalidSchema, ConnectionError
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import random


def get_links(url):
    """Function for getting all links from the webpage"""
    try:
        response = requests.get(url)
    except InvalidSchema as err:
        print(f"Invalid schema: {err}")
        return []
    except ConnectionError as err:
        print(f"Connection error: {err}")
        return []

    bs = BeautifulSoup(response.text, "html.parser")
    links = bs.find_all("a", href=True)
    absolutes = [urljoin(url, link["href"]) for link in links]

    return absolutes


def pop_last_link(list, counter):
    """Function for deleting last element from list, setting previous last
    element as current url and decreasing counter"""
    try:
        list.pop()
    except IndexError:
        print("Empty list of links - can't go back")
        exit()
    counter = counter - 1
    url = list[counter - 1]

    return url, counter


def write_results(results, filename, header, type="list"):
    with open(filename, "w") as file:
        file.write(header)  # nagłówek

        if type == "list":
            for i in range(len(results)):
                file.write(f"{i+1};{results[i]}\n")  # poszczególne linie
        elif type == "dict":
            i = 1
            for k, v in results.items():
                file.write(f"{i};{k};{v}\n")
                i = i + 1


def main():
    # Initialization
    counter = 0
    iterations = 0
    links_list = []
    links_checked_dict = {}

    # Starting webpage
    website_url = "https://onet.pl"  # input("Enter the URL link of a webpage you want to crawl: ")

    # Main loop
    while counter < 100:
        # Counting n of total iterations for statistics' purposes
        iterations = iterations + 1

        # Controling how many times given link has been checked (after 10 checks it is deleted from list)
        links_checked_dict[website_url] = (
            links_checked_dict[website_url] + 1
            if website_url in links_checked_dict.keys()
            else 1
        )

        if links_checked_dict[website_url] >= 10:
            print(
                f"{website_url} has been checked 10 times or more! Deleting & going back"
            )
            website_url, counter = pop_last_link(links_list, counter)
            continue

        # Get all links from the website
        links = get_links(website_url)

        # N of links
        n = len(links)

        # If there were no links on the page or there was invalid schema of link
        if n == 0:
            print(
                f"Problem with {website_url}: deleting it from list & going up (number of list elements: {counter})"
            )
            website_url, counter = pop_last_link(links_list, counter)
            continue

        # Getting random link
        link = links[random.randint(0, n - 1)]

        # If the link is already in the list
        if link in website_url:
            if n == 1:  # If it was the only link available we can immediately go back
                print(
                    f"Page {website_url} has only one link and it's itself: deleting it from list & going up (number of list elements: {counter})"
                )
                website_url, counter = pop_last_link(links_list, counter)
            continue  # If not it goes the 'normal' way - it will be checked up to 10 times

        # Setting drawn link as url to crawl
        website_url = link

        # Adding aforementioned link to the list
        links_list.append(link)
        print(link)

        # Cunter of elements in final list
        counter = counter + 1

    # Printing results
    print("\nSuccess!")
    print(f"Total number of iterations: {iterations}")
    print("Checked links:")
    for k, v in links_checked_dict.items():
        print(f"{k}: {v}")
    print(f"Links:{links_list}")

    write_results(links_list, "links_list.txt", "n;url\n")
    write_results(links_checked_dict, "links_checked.txt", "n;key;value\n", "dict")


if __name__ == "__main__":
    main()
