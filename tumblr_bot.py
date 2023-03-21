import sys
import pytumblr
import random
import settings
import horse_gen


def create_post(horse, client = None, blog = None, real=True):
    try:
        name, story, link = horse_gen.get_info(horse)
    except Exception as e:
        new_horse = pick_horse()
        create_post(new_horse, client, blog) 
        sys.exit(1)
    title = f"Random Real Thoroughbred: {name}"
    body = f"{story}<hr><hr>Link to their pedigreequery page: <a href={link}>{link}</a>"
    if horse == "/at+the+station2":
        body += "<hr>Wow, this is my horse, what are the odds?"
    if real:
        client.create_text(blog, state="published", title=title, body=body, tags=[horse]) 
    else:
        print(name, story, link, sep="\n")


def pick_horse():
    horse_list = settings.horse_list
    horse = random.choice(horse_list)
    return horse

def main():
    client = pytumblr.TumblrRestClient(
    settings.key,
    settings.key_secret,
    settings.token,
    settings.token_secret)

    blog = settings.blog_name
    horse = pick_horse()
    create_post(horse, client, blog)
    
if __name__ == '__main__':
    main()
