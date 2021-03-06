import sys
import json
import random
from urllib import request


class Quote:
    def __init__(self, author, quote):
        self.author = author
        self.quote = quote


def import_all(filename):
    f = open(filename, "r")
    data = json.load(f)
    f.close()
    return [Quote(d["author"], d["quote"]) for d in data]


def pretty_print(quote):
    print(quote.author + "\t" + quote.quote)


def random_quote(collection):
    return collection[random.randint(0, len(collection) - 1)]


def print_help():
    print("this is the help")  # todo make the help


def retrieve_from_json(json_response, dict_keys_values):
    data = json.load(json_response)
    return [Quote(d[dict_keys_values["author"]], d[dict_keys_values["quote"]]) for d in data]


# todo Set the project to support only one general provider
def retrieve_quotes_from_talaikis():
    req = request.Request("https://talaikis.com/api/quotes/")
    try:
        response = request.urlopen(req)
        quotes = retrieve_from_json(response, {"author": "author", "quote": "quote"})
        return quotes
    except request.URLError:
        return []


def populate_file(filename, quotes):
    f = open(filename, "w")
    f.write("[")
    for i in range(len(quotes)):
        quote = quotes[i]
        data = {"author": quote.author, "quote": quote.quote}
        f.write(json.dumps(data))
        if i < len(quotes) - 1:
            f.write(",")
    f.write("]")
    f.close()


if __name__ == '__main__':
    args = sys.argv[1:]
    if len(args) == 1 and args[0] == "-h":
        print_help()
    elif len(args) == 1 and args[0] == "--populate":
        downloaded_quotes = retrieve_quotes_from_talaikis()
        populate_file("data/quotes", downloaded_quotes)
    elif len(args) == 0:
        da = import_all("data/quotes")
        pretty_print(random_quote(da))
    else:
        print("Error of syntax")
    exit(0)
