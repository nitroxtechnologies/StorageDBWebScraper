#! python3
from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup
from unit import Unit
from selenium import webdriver

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

def parse_GSP():
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

    return units

def parse_PS_beecave():
    raw_html = simple_get('https://www.publicstorage.com/texas/self-storage-bee-cave-tx/78738-self-storage/2190#/?zl=16&vd=0.47440338227124196&lat=0&lng=0&sort=dasc&ssort=dasc&vsort=dasc&v20=0&v35=0&v50=0&vc=0&vu=0&ve=0&cc=0&da=0&ms=1,2,3,4,5,6,7,8')
    html = BeautifulSoup(raw_html, "html.parser")
    units = []

    unitSizes = html.find_all("div", class_= "srp_label srp_font_14")
    for s in unitSizes:
        units.append(Unit("", "", s.text.strip()))
    unitNames = html.find_all("div", class_="srp_label plp", limit = len(units))
    for i, d in enumerate(unitNames):
        units[i].setName(d.text.strip())
    unitPrices = html.find_all("div", class_ = "srp_label alt-price")
    for i, p in enumerate(unitPrices):
        units[i].setPrice(p.text.strip())
    return units

def parse_stowaway():
    # raw_html = simple_get('https://www.lakewayselfstorage.com/units-available/')
    browser = webdriver.Safari()
    browser.get("https://www.lakewayselfstorage.com/units-available/")
    raw_html = browser.page_source
    html = BeautifulSoup(raw_html, "html.parser")
    print(html)
    units = []

    unitSizes = html.find_all("div", class_= "size_txt")
    for s in unitSizes:
        units.append(Unit("", "", s.text.strip()))
    unitNames = html.find_all("span", class_="ls_unit_area", limit = len(units))
    for i, d in enumerate(unitNames):
        units[i].setName(d.text.strip())
    unitPrices = html.find_all("span", class_ = "ls_unit_price")
    for i, p in enumerate(unitPrices):
        units[i].setPrice(p.text.strip())
    return units

def parse_southlake():
    raw_html = simple_get('http://www.southlakewarehouses.com/pages/rent')
    html = BeautifulSoup(raw_html, "html.parser")
    units = []

    unitSizes = html.find_all("h4", class_= "primary-color")
    for s in unitSizes:
        units.append(Unit("", "", s.text.strip()))
    unitNames = html.find_all("p", class_="unit-description", limit = len(units))
    for i, d in enumerate(unitNames):
        units[i].setName(d.text.strip())
    unitPrices = html.find_all("strong", class_ = "price primary-color pull-right")
    for i, p in enumerate(unitPrices):
        units[i].setPrice(p.text.strip())
    return units

def main():
    GSP = parse_GSP()
    print("================ GREEN STORAGE PLUS ================")
    for u in GSP:
        print(u)
    print("====================================================")

    PS = parse_PS_beecave()
    print("============= PUBLIC STORAGE @ BEE CAVE ============")
    for u in PS:
        print(u)
    print("====================================================")

    SL = parse_southlake()
    print("================ SOUTHLAKE WAREHOUSES ==============")
    for u in SL:
        print(u)
    print("====================================================")

if __name__ == "__main__":
    main()
