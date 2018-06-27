#! python3
from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup
from unit import Unit
from facility import Facility
from selenium import webdriver
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

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

def parse_GSP(website):
    # website = input("Enter Green Storage Plus facility website: ")
    raw_html = simple_get(website)
    html = BeautifulSoup(raw_html, "html.parser")
    units = []

    name = html.find_all("span",  attrs={"itemprop":"name"})[0].text.strip()
    street = html.find_all("div", attrs={"itemprop":"streetAddress"})[0].text.strip()
    city = html.find_all("span", attrs={"itemprop":"addressLocality"})[0].text.strip()
    state = html.find_all("span", attrs={"itemprop":"addressRegion"})[0].text.strip()
    zip = html.find_all("span", attrs={"itemprop":"postalCode"})[0].text.strip()
    address = street + ", " + city + ", " + state + " " + zip

    unitSizes = html.find_all("div", class_= "container size")
    for s in unitSizes:
        units.append(Unit(s.text.strip(), "", "", ""))
    unitNames = html.find_all("div", class_="description pure-visible-sm", limit = len(units))
    for i, d in enumerate(unitNames):
        # print(d)
        desc = d.text.strip()
        if "Climate" in desc:
            units[i].setType("Climate")
        elif "Drive" in desc:
            units[i].setType("Parking")
        else:
            units[i].setType("Non-Climate")
        if "Ground" in desc:
            units[i].setFloor("1")
    unitPrices = html.find_all("div", class_ = "price")
    for i, p in enumerate(unitPrices):
        units[i].setPrice(p.text.strip())

    return Facility("Green Storage Plus", "https://https://www.greenstorageplus.com/" ,name, website, address, units)

def parse_EZ():
    raw_html = simple_get('https://e-zlakewaystorage.com/services-and-pricing/')
    html = BeautifulSoup(raw_html, "html.parser")
    units = []

    unitSizes = html.find_all("strong")
    for s in unitSizes:
        if len(s.text.strip()) < 5:
            units.append(Unit(s.text.strip(), "", "", ""))

    # unitNames = html.find_all("div", class_="description", limit = len(units))
    # for i, d in enumerate(unitNames):
    #     units[i].setName(d.text.strip())
    # unitPrices = html.find_all("div", class_ = "price")
    # for i, p in enumerate(unitPrices):
    #     units[i].setPrice(p.text.strip())

    return units

def parse_PS(website):
    raw_html = simple_get(website)
    html = BeautifulSoup(raw_html, "html.parser")
    units = []

    # facilityTitle = html.find_all("span",  attrs={"id":"FacilityTitle"})
    street = html.find_all("span", attrs={"itemprop":"streetAddress"})[0].text.strip()
    city = html.find_all("span", attrs={"itemprop":"addressLocality"})[0].text.strip()
    state = html.find_all("span", attrs={"itemprop":"addressRegion"})[0].text.strip()
    zip = html.find_all("span", attrs={"itemprop":"postalCode"})[0].text.strip()
    address = street + ", " + city + ", " + state + " " + zip
    name = address

    unitSizes = html.find_all("div", class_= "srp_label srp_font_14")
    for s in unitSizes:
        units.append(Unit(s.text.strip(), "", "", ""))
    unitPrices = html.find_all("div", class_ = "srp_label alt-price")
    for i, p in enumerate(unitPrices):
        units[i].setPrice(p.text.strip().split("/")[0])
    features = []
    for divtag in html.find_all('div', {'class': 'srp_res_clm srp_clm120'}):
        for i, ultag in enumerate(divtag.find_all('ul')):
            string = ""
            for litag in ultag.find_all('li'):
                string+=litag.text + " "
            features.append(string)
    for i, f in enumerate(features):
        if "Climate" in f:
            units[i].setType("Climate")
        else:
            units[i].setType("Non-Climate")
        if "1st" in f:
            units[i].setFloor("1")
        else:
            units[i].setFloor("2")
        # index = f.find('st')
        # if index < 0:
        #     units[i].setFloor("Ground")
        # else:
        #     units[i].setFloor(f[index-1])
    return Facility("Public Storage", "https://www.publicstorage.com/", name, website, address, units)

def parse_stowaway(website):
    # raw_html = simple_get('https://www.lakewayselfstorage.com/units-available/')
    browser = webdriver.Safari()
    browser.get(website)
    try:
        browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        element = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "targetContainer"))
        )
        # browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        # element = WebDriverWait(browser, 10).until(
        #     EC.visibility_of_element_located((By.ID, "ember945"))
        # )
        raw_html = browser.page_source
        html = BeautifulSoup(raw_html, "html.parser")
        # print(html)
        units = []

        name = html.find_all("strong",  attrs={"itemprop":"name"})[0].text.strip()

        # street = html.find_all("p", attrs={"itemprop":"streetAddress"})[0].text.strip()
        # city = html.find_all("span", attrs={"itemprop":"addressLocality"})[0].text.strip()
        # state = html.find_all("span", attrs={"itemprop":"addressRegion"})[0].text.strip()
        # zip = html.find_all("span", attrs={"itemprop":"postalCode"})[0].text.strip()
        # address = street + ", " + city + ", " + state + " " + zip
        address = html.find_all("span", attrs={"itemprop":"address"})[0].text.strip()

        unitSizes = html.find_all("div", class_= "size_txt")
        for s in unitSizes:
            units.append(Unit(s.text.strip(), "", "", ""))
        unitNames = html.find_all("span", class_="ls_unit_area", limit = len(units))
        for i, d in enumerate(unitNames):
            units[i].setName(d.text.strip())
        unitPrices = html.find_all("span", class_ = "ls_unit_price")
        for i, p in enumerate(unitPrices):
            units[i].setPrice(p.text.strip())
    finally:
        browser.quit()

    return Facility("Stowaway", "https://www.selfstoragelakeway.com/l", name, website, address, units)

def parse_southlake():
    raw_html = simple_get('http://www.southlakewarehouses.com/pages/rent')
    html = BeautifulSoup(raw_html, "html.parser")
    units = []

    unitSizes = html.find_all("h4", class_= "primary-color")
    for s in unitSizes:
        units.append(Unit(s.text.strip(), "", "", ""))
    unitNames = html.find_all("p", class_="unit-description", limit = len(units))
    for i, d in enumerate(unitNames):
        units[i].setName(d.text.strip())
    unitPrices = html.find_all("strong", class_ = "price primary-color pull-right")
    for i, p in enumerate(unitPrices):
        units[i].setPrice(p.text.strip())
    return units

def parse_cubesmart(website):
    browser = webdriver.Safari()
    browser.get(website)
    raw_html = browser.page_source
    html = BeautifulSoup(raw_html, "html.parser")
    units = []
    # print(html)
    name = html.find_all("h1",  attrs={"class":"csCBE"})[0].text.strip()
    street = html.find_all("p", attrs={"itemprop":"streetAddress"})[0].text.strip()
    city = html.find_all("span", attrs={"itemprop":"addressLocality"})[0].text.strip()
    state = html.find_all("span", attrs={"itemprop":"addressRegion"})[0].text.strip()
    zip = html.find_all("span", attrs={"itemprop":"postalCode"})[0].text.strip()
    address = street + ", " + city + ", " + state + " " + zip

    unitSizes = html.find_all("p", attrs={"itemprop":"name"})
    for s in unitSizes:
        units.append(Unit(s.text.strip(), "", "", ""))
        # print(s.text.strip())
    unitPrices = html.find_all("div", class_ = "promoprice showVdm")
    for i, p in enumerate(unitPrices):
        units[i].setPrice("$" + p['content'])
    browser.quit()
    return Facility("Cubesmart", "https://www.cubesmart.com/", name, website, address, units)
    # units = []
    #
    # unitSizes = html.find_all("h4", class_= "primary-color")
    # for s in unitSizes:
    #     units.append(Unit("", "", s.text.strip()))
    # unitNames = html.find_all("p", class_="unit-description", limit = len(units))
    # for i, d in enumerate(unitNames):
    #     units[i].setName(d.text.strip())
    # unitPrices = html.find_all("strong", class_ = "price primary-color pull-right")
    # for i, p in enumerate(unitPrices):
    #     units[i].setPrice(p.text.strip())
    # return units


def parse_extra(website):
    browser = webdriver.Safari()
    # website = input("Enter ExtraSpace facility website: ")
    browser.get(website)
    raw_html = browser.page_source
    html = BeautifulSoup(raw_html, "html.parser")
    units = []
    # print(html)
    facilityTitle = html.find_all("span",  attrs={"id":"FacilityTitle"})
    street = html.find_all("span", attrs={"itemprop":"streetAddress"})[0].text.strip()
    city = html.find_all("span", attrs={"itemprop":"addressLocality"})[0].text.strip()
    state = html.find_all("span", attrs={"itemprop":"addressRegion"})[0].text.strip()
    zip = html.find_all("span", attrs={"itemprop":"postalCode"})[0].text.strip()
    address = street + ", " + city + ", " + state + " " + zip

    # print(facilityTitle)
    name = facilityTitle[0].text.strip()
    # print("Loading units for " + name + "....")
    unitSizes = html.find_all("div", attrs={"itemprop":"description"})
    for s in unitSizes:
        if len(s.text.strip()) < 10:
            units.append(Unit(s.text.strip(), "", "", ""))
    unitPrices = html.find_all("div", attrs={"itemprop":"price"})
    for i, p in enumerate(unitPrices):
        units[i].setPrice(p['content'])

    features = []
    for divtag in html.find_all('div', {'class': 'features'}):
        for i, ultag in enumerate(divtag.find_all('ul')):
            string = ""
            for litag in ultag.find_all('li'):
                string+=litag.text + " "
            features.append(string)
    for i, f in enumerate(features):
        if "Climate" in f:
            units[i].setType("Climate")
        else:
            units[i].setType("Non-Climate")
        if "1st" in f:
            units[i].setFloor("1")
        else:
            units[i].setFloor("2")
        if "Drive-Up" in f:
            units[i].setType("Parking")
        if "RV Parking" in f:
            units[i].setType("RV Parking")

        # else:
        #     units[i].setFloor("2")

    # unitPrices = html.find_all("div", class_ = "promoprice showVdm")
    # for i, p in enumerate(unitPrices):
    #     units[i].setPrice("$" + p['content'])
    browser.quit()

    return Facility("ExtraSpace" , "https://www.extraspace.com/", name, website, address, units)
    # return units

def parse_amax(website):
    raw_html = simple_get(website)
    html = BeautifulSoup(raw_html, "html.parser")
    units = []

    name = html.find_all("span",  attrs={"itemprop":"name"})[0].text.strip()
    street = html.find_all("div", attrs={"itemprop":"streetAddress"})[0].text.strip()
    city = html.find_all("span", attrs={"itemprop":"addressLocality"})[0].text.strip()
    state = html.find_all("span", attrs={"itemprop":"addressRegion"})[0].text.strip()
    zip = html.find_all("span", attrs={"itemprop":"postalCode"})[0].text.strip()
    address = street + ", " + city + ", " + state + " " + zip

    unitSizes = html.find_all("div", class_= "container size")
    for s in unitSizes:
        units.append(Unit(s.text.strip(), "", "", ""))
        # print(s.text.strip())
    unitNames = html.find_all("div", class_="description pure-visible-sm", limit = len(units))
    for i, d in enumerate(unitNames):
        # print(d)
        desc = d.text.strip()
        # print(desc)
        if "A/C" in desc:
            units[i].setType("Climate")
        elif "Parking" in desc:
            units[i].setType("Parking")
        else:
            units[i].setType("Non-Climate")
        # if "Ground" in desc:
        #     units[i].setFloor("1")
    unitPrices = html.find_all("div", class_ = "price")
    for i, p in enumerate(unitPrices):
        units[i].setPrice(p.text.strip())

    return Facility("A-Max Self Storage", "https://www.amaxselfstorage.com/", name, website, address, units)

def parse_storeitall(website):
    browser = webdriver.Safari()
    browser.get(website)
    try:
        element = WebDriverWait(browser, 10).until(
            EC.visibility_of_element_located((By.CLASS_NAME, "unit-info"))
        )
        browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        element = WebDriverWait(browser, 10).until(
            EC.visibility_of_element_located((By.ID, "ember940"))
        )
        raw_html = browser.page_source
        html = BeautifulSoup(raw_html, "html.parser")
        units = []

        name = html.find_all("h4",  attrs={"class":"p-name"})[0].text.strip()
        street = html.find_all("span", attrs={"class":"p-street-address"})[0].text.strip()
        city = html.find_all("span", attrs={"class":"p-locality"})[0].text.strip()
        state = html.find_all("span", attrs={"class":"p-region"})[0].text.strip()
        zip = html.find_all("span", attrs={"class":"p-postal-code"})[0].text.strip()
        address = street + ", " + city + ", " + state + " " + zip

        unitSizes = html.find_all("span", attrs={"class":"sss-unit-size"})
        for s in unitSizes:
            if len(s.text.strip()) < 10:
                units.append(Unit(s.text.strip(), "", "", ""))
        unitPrices = html.find_all("span", attrs={"class":"sss-unit-special"})
        for i, p in enumerate(unitPrices):
            prices = p.find_all("span", attrs={"class":"price-value"})
            if len(prices) == 0:
                units[i].setPrice("0")
            else:
                units[i].setPrice(prices[0].text.strip())

        # unitAmenities = html.find_all("span", attrs={"class":"sss-unit-amenities"})
        # for i, p in enumerate(unitAmenities):
        #     if "Climate Control" in p.text:
        #         units[i].setType("Climate")
        #     else:
        #         units[i].setType("Non-Climate")
        unitTypes = html.find_all("div", attrs={"class":"sss-unit-description"})
        for i, t in enumerate(unitTypes):
            if "Non Climate" in t.text:
                units[i].setType("Non-Climate")
            elif "Parking" in t.text:
                units[i].setType("Parking")
            else:
                units[i].setType("Climate")

    finally:
        browser.quit()

    return Facility("Store-It-All Storage", "https://www.amaxselfstorage.com/",name, website, address, units)


def main():
    with open('facilities', 'r') as file:
        # with open('units.txt', 'w') as out:
        facilities = file.readlines()
        facilities = [line.rstrip('\n') for line in open('facilities')] # strip newline character
        for f in facilities:
            if "extraspace" in f:
                print(parse_extra(f).printInfo(), end='')
            elif "greenstorageplus" in f:
                print(parse_GSP(f).printInfo(), end='')
            elif "cubesmart" in f:
                print(parse_cubesmart(f).printInfo(), end='')
            elif "publicstorage" in f:
                print(parse_PS(f).printInfo(), end='')
            elif "amaxselfstorage" in f:
                print(parse_amax(f).printInfo(), end='')
            elif "lakewayselfstorage" in f:
                print(parse_stowaway(f).printInfo(), end='')
            elif "selfstoragelakeway" in f:
                print(parse_storeitall(f).printInfo(),end='')
        file.close()
            # print("\n\nWebsites scraped:")
            # for s in facilities:
            #     print(s + "\n")

if __name__ == "__main__":
    main()
