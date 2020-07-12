

1) open the terminal in project location

2) setup-
pip install virtualenv
sudo /usr/bin/easy_install virtualenv
virtualenv -p python3 venv
source venv/bin/activate
pip install -r requirements.txt
export FLASK_APP=server.py

3) run server locally-
python -m flask run

4) tests - input in your browser
    A) go to the Swagger documentation (http://127.0.0.1:5000/) and run sample requests from there
    B) activate the virtual env (source venv/bin/activate) and run mini_tests (python mini_test.py). you can look at the the test_output folder for some fun json files
    C) input some urls into your browser:
    
        http://127.0.0.1:5000/QA/qa-query-url?amazon_url=https://www.amazon.com/dp/B084127MVC/&requests_per_product=2
        
        http://127.0.0.1:5000/QA/qa-query-url?amazon_url=https://www.amazon.com/Apple-Smart-Folio-iPad-11-inch/dp/B0863924SL/&requests_per_product=1
        
        http://127.0.0.1:5000/QA/qa-query-url?amazon_url=https://www.amazon.com/Green-Toys-Airplane-Phthalates-Aeronautical/dp/B008LQXR82?&requests_per_product=3

