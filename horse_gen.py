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


def find_trait(trait_category, d, regex, results, horse):
    trait = re.search(regex, results)
    if trait:
        trait = trait.group()[1:-1]
        try:
            trait = d[trait]
            return trait
        except KeyError:
            record_KeyError(trait_category, trait, results, horse)
    return f"{trait_category.upper()} Not Recorded"


def find_country(results, horse):
    return find_trait("country", countries, "\(.*?\)", results, horse)


def find_color(results, horse):
    return find_trait("color", colors, " [a-zA-Z\/a-zA-z]+\.", results, horse)


def find_sex(results, horse):
    return find_trait("sex", sexes, " [A-Z]+,", results, horse)


def record_KeyError(trait, missing_key, results, horse):
    with open("dict_problems.txt", "a") as f:
        f.write(f"\n{trait}: {missing_key} \n{results}\n{horse}\n")
