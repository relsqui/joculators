#!/usr/bin/python3

from bs4 import BeautifulSoup

def extract_quotes(data):
    page = BeautifulSoup(data, "html.parser")

    quotenodes = page.find(id="mw-content-text").find_all("ul", recursive=False)
    quotes = []
    for node in quotenodes:
        try:
            quote = node.li
            source = quote.ul.extract()
            quote_text = quote.text.strip().replace("\n", " / ")
            source_text = source.text.strip().replace("\n", " / ")
            quotes.append("{0} ({1})".format(quote_text, source_text))
        except AttributeError:
            pass
    return quotes

def twitter_filter(string):
    if len(string) > 140:
        return False
    if not all(ord(c) < 128 for c in string):
        return False
    return True

if __name__ == "__main__":
    import sys
    print("\n".join(filter(twitter_filter, extract_quotes(sys.stdin))))
