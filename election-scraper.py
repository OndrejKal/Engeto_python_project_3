"""
projekt_3.py: třetí projekt do Engeto Online Python Akademie

author: Ondřej Kalvas
email: kalvasondrej@gmail.com
discord: Ondřej K.#0612
"""

import requests
from bs4 import BeautifulSoup
import csv
import sys

#url:"https://volby.cz/pls/ps2017nss/ps3?xjazyk=CZ"

def find_parser(url):
    response = requests.get(url)
    return BeautifulSoup(response.text, "html.parser")
def find_all_cities(url):
    soup = find_parser(url)
    cities = soup.find_all("tr")
    return cities
def find_code_and_town(url):
    town = []
    cities = find_all_cities(url)
    for city in cities:
        city_code = city.find("td", {"class": "cislo"})
        city_name = city.find("td", {"class": "overflow_name"})
        if city_code:
            town.append([city_code.text, city_name.text])
        else:
            continue
    return town

def find_url_cities(url):
    cities = find_all_cities(url)
    url_of_cities = []
    for city in cities:
        link = city.find("a", href=True)
        if link:
            url_of_cities.append("https://volby.cz/pls/ps2017nss/" + link["href"])
        else:
            continue
    return url_of_cities

def find_voter_turnout(url_of_cities):
    voters_stats = []
    for url in url_of_cities:
        soup = find_parser(url)
        election_table = soup.find("table", {"class": "table"})
        voters_in_the_list = election_table.find_all("td", {"class": "cislo"})[3]. text.replace("\xa0", "")
        released_envelopes = election_table.find_all("td", {"class":"cislo"})[4].text.replace("\xa0", "")
        valid_votes = election_table.find_all("td", {"class": "cislo"})[7].text.replace("\xa0", "")
        voters_stats.append([voters_in_the_list, released_envelopes, valid_votes])
    return voters_stats

def find_party_votes(url_of_cities):
    votes = []
    for url in url_of_cities:
        soup = find_parser(url)
        table = soup.find_all("div", {"class": "t2_470"})
        whole_table = []
        lines = []
        total_votes = []

        for vote in table:
            table_lines = vote.find_all("tr")
            whole_table.extend(table_lines)

        for all in whole_table:
            table_line = all.find_all("td", {"class": "cislo"})
            if table_line:
                lines.append(table_line)
            else:
                continue

        for line in lines:
            total_votes.append(line[1].text.replace("\xa0", ""))
        votes.append(total_votes)
    return votes

def find_party_names(url_of_cities):
    party_names = []
    soup = find_parser(url_of_cities)
    names_in_table = soup.find_all("td", {"class": "overflow_name"})
    for name in names_in_table:
        party_names.append(name.text)
    return party_names

def create_table(url):
    link = find_url_cities(url)[0]
    head = ["code", "location", "registered", "envelopes", "valid"]
    party_names = find_party_names(link)
    head.extend(party_names)
    return head

def results(url):
    url_of_cities = find_url_cities(url)
    results = find_code_and_town(url)
    voters_stats = find_voter_turnout(url_of_cities)
    party_results = find_party_votes(url_of_cities)
    for i in range(len(results)):
        results[i].extend(voters_stats[i])
    for j in range(len(results)):
        results[j].extend(party_results[j])
    return results

def create_csv(url, file_name):
    print(f"I'm downloading data from the selected url: {url}")
    village = results(url)
    head = create_table(url)
    print(f"I'm just saving it to a file: {file_name}")
    with open(file_name, "w", newline="", encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(head)
        for line in village:
            writer.writerow(line)

def main():
    if len(sys.argv) != 3:
       print("enter the url of the link and the name of the file.csv to start the program")
    elif ".csv" in sys.argv[1] and "volby.cz/" in sys.argv[2]:
        print("you changed the order of the arguments, enter them correctly")
    elif "volby.cz/pls/ps2017nss/" not in sys.argv[1]:
        print("you are providing an invalid link")
    elif ".csv" not in sys.argv[2]:
        print("the file name must end with .csv")
    else:
        create_csv(sys.argv[1], sys.argv[2])
    print("I'm quitting election-scraper")

if __name__ == "__main__":
    main()