
from amazon_parser import AmazonParser
from amazon_http_request import AmazonHttpRequest


class AmazonCrawler:

    def __init__(self):
        self.page_limit = 10
        self.parser = AmazonParser()
        self.requests = AmazonHttpRequest()
        self.question_page_format = "https://www.amazon.com/ask/questions/asin/{asin}/{page_number}/"

    def product_page_crawl(self, product_page_url):
        asin = self.parser.get_asin_from_url(product_page_url)
        return asin

    def question_page_crawl(self, asin, desired_number_of_pages):
        qa_data = []
        for i in range(min(desired_number_of_pages, self.page_limit)):
            questions_url = self.question_page_format.format(asin=asin, page_number=i+1)
            page_content = self.requests.get(questions_url)
            parsed_page, next_question_url = self.parser.parse_multi_question_url(page_content)
            qa_data.extend(parsed_page)

            if not next_question_url:
                # if there is no next button we have reached the end of the crawler
                break
        return qa_data

