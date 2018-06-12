#! python3
from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup
from unit import Unit

def simple_get(url):
    """
    Attempts to get the content at `url` by making an HTTP GET request.
    If the content-type of response is some kind of HTML/XML, return the
    text content, otherwise return None
    """
    try:
        with closing(get(url, stream=True)) as resp:
            if is_good_response(resp):
                return resp.content
            else:
                return None

    except RequestException as e:
        log_error('Error during requests to {0} : {1}'.format(url, str(e)))
        return None


def is_good_response(resp):
    """
    Returns true if the response seems to be HTML, false otherwise
    """
    content_type = resp.headers['Content-Type'].lower()
    return (resp.status_code == 200
            and content_type is not None
            and content_type.find('html') > -1)


def log_error(e):
    print(e)

def main():
    raw_html = simple_get('https://www.greenstorageplus.com/self-storage-spicewood-tx-f7744')
    html = BeautifulSoup(raw_html, "html.parser")
    units = []

    unitSizes = html.find_all("div", class_= "container size")
    for s in unitSizes:
        units.append(Unit("", "", s.text.strip()))

    unitNames = html.find_all("div", class_="description", limit = len(units))
    for i, d in enumerate(unitNames):
        units[i].setName(d.text.strip())

    unitPrices = html.find_all("div", class_ = "price")
    for i, p in enumerate(unitPrices):
        units[i].setPrice(p.text.strip())

    for u in units:
        print(u)

if __name__ == "__main__":
    main()
