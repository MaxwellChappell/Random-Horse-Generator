import pytumblr
import random
import settings
import re


def format_name(horse):
    #removes / in the URL and numbers at the end
    ret = re.sub("[\/]|\d+$", "", horse)
    #removes + seperators
    ret = re.sub("\+", " ", ret)
    ret = ret.upper()
    return ret


client = pytumblr.TumblrRestClient(
    settings.key,
    settings.key_secret,
    settings.token,
    settings.token_secret)

blog = settings.blog_name
horse_list = settings.horse_list

horse = random.choice(horse_list)

print(horse)
print(format_name(horse))
