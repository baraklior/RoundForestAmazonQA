
import requests


class AmazonHttpRequest:

    def __init__(self):
        self.base_address = "https://www.amazon.com/"
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'}

    def get(self, url):
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.content

