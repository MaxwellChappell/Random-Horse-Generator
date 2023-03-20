import pytumblr
import random
import settings
import re
import requests
from bs4 import BeautifulSoup
import conversion_dicts

sexes = conversion_dicts.sexes
countries = conversion_dicts.countries
colors = conversion_dicts.colors


def format_name(horse):
    # removes / in the URL and numbers at the end
    ret = re.sub("[\/]|\d+$", "", horse)
    # removes + seperators
    ret = re.sub("\+", " ", ret)
    ret = ret.upper()
    return ret


def create_post(horse):
    title = f"Random Real Thoroughbred: {format_name(horse)}"
    body = f"Link to their pedigreequery page: \n <a href=\"https://www.pedigreequery.com{horse}\">https://www.pedigreequery.com{horse}</a>"
    if horse == "/at+the+station2":
        body += "<hr>Wow, this is my horse, what are the odds?"
    client.create_text(blog, state="published", title=title, body=body)


def get_info(horse):
    url = "https://www.pedigreequery.com" + horse
    page = requests.get(url)

    soup = BeautifulSoup(page.content, "html.parser")

    results = soup.find_all("td", {"data-g": "1"})

    sire = "Not Recorded"
    dame = "Not Recorded"
    for line in results:
        if "f" in line["class"]:
            dame = line.find("a").text
        elif "m" in line["class"]:
            sire = line.find("a").text

    results = soup.find("font").text.split(
        "\n")[0][len(horse):]

    print(results)
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

    print(repr(results))
    story = f"{format_name(horse)} is a {color} {sex} born in {country} in {year}"
    print(story)


client = pytumblr.TumblrRestClient(
    settings.key,
    settings.key_secret,
    settings.token,
    settings.token_secret)

blog = settings.blog_name
horse_list = settings.horse_list

for i in range(100):
    horse = random.choice(horse_list)

    print(horse)
    get_info(horse)
    print()
# create_post("/at+the+station2")
