import pytumblr
import random
import settings
import horse_gen

def create_post(horse):

    title = f"Random Real Thoroughbred: {format_name(horse)}"
    body = f"Link to their pedigreequery page: \n <a href=\"https://www.pedigreequery.com{horse}\">https://www.pedigreequery.com{horse}</a>"
    if horse == "/at+the+station2":
        body += "<hr>Wow, this is my horse, what are the odds?"
    client.create_text(blog, state="published", title=title, body=body)

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
    name, story, link = horse_gen.get_info(horse)
    print(name, story, link, sep="\n")
    print()
# create_post("/at+the+station2")
