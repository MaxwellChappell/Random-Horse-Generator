import horse_gen
import settings
import horse_gen
import itertools
import random
import tumblr_bot


def test_story():
    name = "test"
    color = "bay"
    sex = "mare"
    country = "US"
    year = 1984
    sire = "dad"
    dam = "mom"
    fail = "Not Recorded"

    lst = list(itertools.product([0, 1], repeat=6))

    for i in lst:
        things = [color, sex, country, year, sire, dam]
        things = [item if i[index] == 1 else fail for index,
                  item in enumerate(things)]
        print(things, horse_gen.create_story(name, *things), "", sep="\n")


def run_without_posting(n):
    blog = settings.blog_name
    horse_list = settings.horse_list
    for i in range(n):
        horse = random.choice(horse_list)
        tumblr_bot.create_post(horse, False)
        print()


run_without_posting(100)
