import pytumblr
import sys
import settings

client = pytumblr.TumblrRestClient(
    settings.key,
    settings.key_secret,
    settings.token,
    settings.token_secret)

blog = settings.blog_name

client.create_quote(blog, state="published",
                    quote="Hello, World!", source="testing tumblr api")
