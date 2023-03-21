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

    sire, dam = find_parents(soup)

    info_string = soup.find("font")
    name = info_string.find("a").text

    info_string = info_string.text.split("\n")[0].replace(name, "")

    year = find_year(info_string)
    country = find_country(info_string, horse)
    color = find_color(info_string, horse)
    sex = find_sex(info_string, horse)

    story = create_story(name, color, sex, country, year, sire, dam)

    return name, story, url


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
        return "Not Recorded"


def find_country(info, horse):
    return find_trait("country", countries, "\(.*?\)", info, horse)


def find_color(info, horse):
    return find_trait("color", colors, " [a-zA-Z\/a-zA-z]+\.", info, horse)


def find_sex(info, horse):
    return find_trait("sex", sexes, " [A-Z]+,", info, horse)


def find_trait(trait_category, d, regex, results, horse):
    trait = re.search(regex, results)
    if trait:
        trait = trait.group()[1:-1]
        try:
            trait = d[trait]
            return trait
        except KeyError:
            record_KeyError(trait_category, trait, results, horse)
    return "Not Recorded"


def record_KeyError(trait, missing_key, results, horse):
    with open("dict_problems.txt", "a") as f:
        f.write(f"\n{trait}: {missing_key} \n{results}\n{horse}\n")

def create_story(name, color, sex, country, year, sire, dam):
    reject = "Not Recorded"
    if "Not Recorded" not in (name, color, sex, country, year, sire, dam):
        return f"{name} is a {color} {sex} born in {country} in {year}. By {sire} out of {dam}."

    story = name
    if reject not in (color, sex):
        story += f" is a {color} {sex}"
    elif color == sex:
        story += " is mysterious creature"
    elif reject in color:
        story += f" is a {sex}"
    else:
        story += f" is a {color} creature"

    if reject not in (country, year):
        story += f" born in {country} in {year}."
    elif country == year:
        story += "."
    elif reject != country:
        story += f" born in {country}."
    else:
        story += f" born in {year}."

    if reject not in (sire, dam):
        story += f" By {sire} out of {dam}."
    elif reject in sire and sire != dam:
        story += f" Out of {dam}."
    elif reject in dam and dam != sire:
        story += f" By {sire}."

    return story
