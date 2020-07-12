from bs4 import BeautifulSoup
import re

class AmazonParser:

    def __init__(self):
        self.asin_pattern = "(?:[/])([A-Z0-9]{10})(?:[\/|\?|\&|\s])"

    def get_asin_from_url(self, product_page_url):
        # no point of retrieving the page because we can get what we want by regex on the url
        # also amazon doesn't give us the full page with a simple get

        match = re.search(self.asin_pattern, product_page_url)
        asin = match.group().strip('/?')
        return asin

    def parse_multi_question_url(self, questions_html):
        next_question_url = None
        soup = BeautifulSoup(questions_html, "lxml")

        if soup.find("title").text == "Robot Check":
            raise RobotParserException(
                "Busted! Amazon blocked the request and tried to use a CAPTCHA on you. try again later")

        next_button = soup.find("li", class_="a-last").find("a")
        if next_button:
                next_question_url = next_button['href']
        question_nodes = soup.find_all('div', class_='a-fixed-left-grid',id=re.compile("question-"))
        all_questions_with_details = [self.parse_single_question_node(q) for q in question_nodes]
        return all_questions_with_details, next_question_url

    @staticmethod
    def parse_single_question_node(question_node):
        parent_node = question_node.parent
        return {
            "question_id": parent_node.find("span", {"class", "askInlineAnswers"})['id'],
            "question_text": parent_node.find("span", {"class", "a-declarative"}).text.strip(),
            "more_answers_relative_link": parent_node.find("a", class_="a-link-normal")["href"],
            "answers": [(parent_node.find("span", {"class": "askLongText"}) or
                         parent_node.find('span', attrs={"class": None})).text.strip()]
        }


class RobotParserException(Exception):
    pass
