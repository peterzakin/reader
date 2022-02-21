import requests

class TwitterClient(object):

    def __init__(self, bearer_token):
        self.bearer_token = bearer_token

    def _get_headers(self):
        headers = {
            "Authorization": "Bearer %s" % self.bearer_token
        }

        return headers

    def get_liked_tweets_for_user_with_id(self, user_id):
        url = "https://api.twitter.com/2/users/%s/liked_tweets?tweet.fields=entities" % user_id
        headers = self._get_headers()
        response = requests.get(url, headers=headers)
        json = response.json()
        return json['data']

    def get_link_info_from_tweets_liked_by_user(self, user_id):
        tweets = self.get_liked_tweets_for_user_with_id(user_id)
        bookmarks = []
        for tweet in tweets:
            if "entities" in tweet and "urls" in tweet['entities']:
                urls = tweet['entities']['urls']
                for link_object in urls:
                    expanded_url = link_object['expanded_url']
                    if "twitter.com" in expanded_url:
                        continue

                    bookmark = {
                        "url": expanded_url,
                        "tweet": {
                            "id":tweet['id'],
                            "text":tweet['text']
                        }
                    }

                    bookmarks.append(bookmark)

        return bookmarks

    def get_user_by_username(self, username):
        """{'data': {'id': '23171244', 'name': 'Peter Zakin', 'username': 'pzakin'}}"""
        url      = "https://api.twitter.com/2/users/by/username/%s" % username
        headers  = self._get_headers()
        response = requests.get(url, headers=headers)
        json     = response.json()

        return json['data']
