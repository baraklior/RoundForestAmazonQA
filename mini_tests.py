import traceback
import requests
import json
import os

test_parameters = [
    ("1",
     lambda json : len(json['qa_data']) == 10,
     "check server recieves and parses 1 question page",
     "http://127.0.0.1:5000/QA/qa-query-url?amazon_url=https://www.amazon.com/Acer-Display-Graphics-Keyboard-A515-43-R19L/dp/B07RF1XD36/&requests_per_product=1"),

    ("2",
     lambda json : json['retrieved_from_cache'] == True,
     "check second call to same page gets info from cache",
     "http://127.0.0.1:5000/QA/qa-query-url?amazon_url=https://www.amazon.com/Acer-Display-Graphics-Keyboard-A515-43-R19L/dp/B07RF1XD36/&requests_per_product=1"),

    ("3",
     lambda json : len(json['qa_data']) == 20,
     "check call with 2 requests per product page sends more answers",
     "http://127.0.0.1:5000/QA/qa-query-url?amazon_url=https://www.amazon.com/dp/B084127MVC/&requests_per_product=2"),

]

def general_test(test_num, test_func, test_purpose, test_url):
    print("test number {}:".format(test_num))
    try:
        json_text = send_request(test_url)
        output_to_json_file(test_num, json_text)
        json_obj = json.loads(json_text)

        if test_func(json_obj):
            print("test {} passed!!!-test purpose: {}".format(test_num, test_purpose))
        else:
            print("test {} failed!!!- test purpose: {}".format(test_num, test_purpose))
    except BaseException as e:
        print("an Exception occured:")
        traceback.print_exc()


def send_request(url):
    res = requests.get(url)
    res.raise_for_status()
    return res.text

def output_to_json_file(test_number, text):
    file_name = "test_output/test{}.json".format(test_number)
    with open(file_name,'w') as out_file:
        out_file.write(text)


def run_all_tests():
    if not os.path.exists('test_output'):
        os.makedirs('test_output')
    for param in test_parameters:
        general_test(*param)

if __name__ == "__main__":
    run_all_tests()
