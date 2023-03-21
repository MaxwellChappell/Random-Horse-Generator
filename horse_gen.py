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

    year = find_year(results)
    country = find_country(results, horse)
    color = find_color(results, horse)
    sex = find_sex(results, horse)

    # print(repr(results))
    story = f"{name} is a {color} {sex} born in {country} in {year}. By {sire} out of {dame}."
    link = f"https://www.pedigreequery.com{horse}"
    return name, story, link


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


def find_year(info):
    year = re.search("\d\d\d\d[\?]*$", info)
    if year:
        return year.group()
    else:
        return "Year Not Recorded"


def find_country(results, horse):
    country = re.search("\(.*?\)", results)
    if country:
        country = country.group()[1:-1]
        try:
            country = countries[country]
            return country
        except KeyError:
            record_KeyError("country", country, results, horse)
    else:
        return "Country Not Recorded"


def find_color(results, horse):
    color = re.search(" [a-zA-Z\/a-zA-z]+\.", results)
    if color:
        color = color.group()[1:-1]
        try:
            color = colors[color]
            return color
        except KeyError:
            record_KeyError("color", color, results, horse)
    else:
        return "Color Not Recorded"


def find_sex(results, horse):
    sex = re.search(" [A-Z]+,", results)
    if sex:
        sex = sex.group()[1:-1]
        try:
            sex = sexes[sex]
            return sex
        except KeyError:
            record_KeyError("sex", sex, results, horse)
    else:
        return "Sex Not Recorded"


def record_KeyError(trait, missing_key, results, horse):
    with open("dict_problems.txt", "a") as f:
        f.write(f"\n{trait}: {missing_key} \n{results}\n{horse}\n")
