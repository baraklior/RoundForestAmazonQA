from flask import Flask, request, jsonify
from flask_restx import Resource, Api, reqparse, fields
from amazon_crawler import AmazonCrawler
from cache_db import CacheDB


app = Flask(__name__)
app.config['RESTPLUS_MASK_SWAGGER'] = False
#for some reason this is not working and the docs still have X-Fields
#look at https://flask-restx.readthedocs.io/en/latest/configuration.html#RESTX_MASK_SWAGGER

api = Api(app,
          version='1.0',
          title='Amazon Q&A Crawler',
          description='Get questions and answers for amazon products')
ns = api.namespace('QA',
                   description='retrieve questions and answers from the Amazon website')

parser = reqparse.RequestParser()
parser.add_argument('amazon_url',
                    required=True,
                    type=str,
                    help='A full amazon product url                 \nfor example:  '
                         'https://www.amazon.com/dp/B084127MVC/')

parser.add_argument('requests_per_product',
                    type=int,
                    required=False,
                    default=1,
                    help='each product has many(up to 1000) answered questions, '
                    'how many pages of questions would you like to retrieve?')

question_model= ns.model('question_data', {
    'question_text': fields.String,
    'question_id': fields.String,
    'answers': fields.List(fields.String),
    'more_answers_relative_link': fields.String,
})

qa_model = ns.model('QA', {
    'requested_url': fields.String,
    'retrieved_from_cache': fields.Boolean,
    'qa_data': fields.List(fields.Nested(question_model)),
})


db = CacheDB()
amazon_crawler = AmazonCrawler()


@ns.route('/qa-query-url')
class QAQueryUrl(Resource):
    @ns.expect(parser)
    @ns.marshal_with(qa_model)
    def get(self):
        args = parser.parse_args(strict=True)
        amazon_url = args['amazon_url']
        number_of_pages = args['requests_per_product']

        asin = amazon_crawler.product_page_crawl(amazon_url)
        if db.is_recently_cached(asin, number_of_pages):
            qa_data = db.get_qa_data(asin)
            retrieved_from_cache = True
        else:
            qa_data = amazon_crawler.question_page_crawl(asin, number_of_pages)
            retrieved_from_cache = False
            db.update_or_insert(asin, qa_data)

        return {"requested_url": amazon_url,
                "qa_data": qa_data,
                "retrieved_from_cache": retrieved_from_cache}
