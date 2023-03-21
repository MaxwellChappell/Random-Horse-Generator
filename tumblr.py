import pytumblr
import random
import settings
import horse_gen


def create_post(horse):
    name, story, link = horse_gen.get_info(horse)
    title = f"Random Real Thoroughbred: {name}"
    body = f"{story}<hr><hr>Link to their pedigreequery page: <a href={link}>{link}</a>"
    if horse == "/at+the+station2":
        body += "<hr>Wow, this is my horse, what are the odds?"
    client.create_text(blog, state="published", title=title, body=body, tag=horse)


client = pytumblr.TumblrRestClient(
    settings.key,
    settings.key_secret,
    settings.token,
    settings.token_secret)

blog = settings.blog_name
horse_list = settings.horse_list

horse = random.choice(horse_list)
create_post(horse)
