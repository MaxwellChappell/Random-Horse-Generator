import conversion_dicts
import re
import requests
from bs4 import BeautifulSoup

sexes = conversion_dicts.sexes
countries = conversion_dicts.countries
colors = conversion_dicts.colors

def get_info(horse):
    url = "https://www.pedigreequery.com" + horse
    page = requests.get(url)

    soup = BeautifulSoup(page.content, "html.parser")

    sire, dame = find_parents(soup)

    results = soup.find("font")
    name = results.find("a").text

    results = results.text.split("\n")[0].replace(name, "")

    year = re.search("\d\d\d\d[\?]*$", results)
    if year:
        year = year.group()
    else:
        year = "Year Not Recorded"

    country = re.search("\(.*?\)", results)
    if country:
        country = country.group()[1:-1]
        try:
            country = countries[country]
        except KeyError:
            with open("dict_problems.txt", "a") as f:
                f.write(f"\ncountry: {country} \n{results}\n{horse}\n")
    else:
        country = "Country Not Recorded"

    color = re.search(" [a-zA-Z\/a-zA-z]+\.", results)
    if color:
        color = color.group()[1:-1]
        try:
            color = colors[color]
        except KeyError:
            with open("dict_problems.txt", "a") as f:
                f.write(f"\ncolor: {color} \n{results}\n{horse}\n")
    else:
        color = "Color Not Recorded"

    sex = re.search(" [A-Z]+,", results)
    if sex:
        sex = sex.group()[1:-1]
        try:
            sex = sexes[sex]

        except KeyError:
            with open("dict_problems.txt", "a") as f:
                f.write(f"\nsex: {sex} \n{results}\n{horse}\n")
    else:
        sex = "Sex Not Recorded"

    #print(repr(results))
    story = f"{name} is a {color} {sex} born in {country} in {year}"

def find_parents(soup):
    results = soup.find_all("td", {"data-g": "1"})
    sire = "Not Recorded"
    dame = "Not Recorded"
    for line in results:
        if "f" in line["class"]:
            dame = line.find("a").text
        elif "m" in line["class"]:
            sire = line.find("a").text
    return sire, dame