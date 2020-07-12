from tinydb import TinyDB, Query
from datetime import datetime
import os


class CacheDB:

    def __init__(self):
        if os.path.exists('questions.json'): os.remove('questions.json')  # deletes the old db from previous runs
        self.inner_db = TinyDB('questions.json')
        self.timestamp_format = '%Y-%m-%d %H:%M:%S'
        self.max_questions_per_page = 10

    def update_or_insert(self, asin, qa_data):
        Product = Query()
        res = self.inner_db.upsert({"asin": asin,
                              "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                              "qa_data": qa_data},
                             Product.asin == asin)
        return res

    def get_qa_data(self, asin):
        Product = Query()
        res = self.inner_db.get(Product.asin == asin)
        return res['qa_data']

    def is_recently_cached(self, asin, desired_requests):
        Product = Query()
        res = self.inner_db.get(Product.asin == asin)
        if not res:
            return False

        number_of_questions_in_db = len(res['qa_data'])
        number_of_desired_questions = desired_requests * self.max_questions_per_page

        timestamp = res['timestamp']
        time_delta = datetime.now() - datetime.strptime(timestamp, self.timestamp_format)

        if time_delta.days <= 1 and number_of_desired_questions <= number_of_questions_in_db:
            return True

        return False



