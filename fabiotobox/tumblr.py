import pytumblr


class Tumblr:
    def __init__(
        self,
        consumer_key: str,
        consumer_secret: str,
        oauth_token: str,
        oauth_secret: str,
        blog_name: str,
    ):
        self.client = pytumblr.TumblrRestClient(
            consumer_key, consumer_secret, oauth_token, oauth_secret
        )
        self.blog_name = blog_name

    def post_photo(self, photo: str, description: str, tags: list):
        self.client.create_photo(
            self.blog_name, state="published", tags=tags, tweet=description, data=photo
        )
