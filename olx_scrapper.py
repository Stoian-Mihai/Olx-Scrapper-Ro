from bs4 import BeautifulSoup
import requests

# This class is used to scrap a single announcement
class olx_scrap_add:
    def __init__(self,link):
        # Downloading the page HTML text
        self.page_link = link
        self.__html_page = requests.get(self.page_link)
    def get_description(self):
        response = self.__html_page
        soup = BeautifulSoup(response.text, 'html.parser')
        description = soup.find_all(class_='clr lheight20 large')
        description = description[0].get_text()
        return description

    def get_title(self):
        response = self.__html_page
        soup = BeautifulSoup(response.text, 'html.parser')
        title = soup.find_all(class_='offer-titlebox')
        aux = title[0]
        title = aux
        i = 42
        title = str(title)
        while title[i] != '<':
            i = i + 1
        return title[42:i]

    def get_price(self):
        response = self.__html_page
        soup = BeautifulSoup(response.text, 'html.parser')
        price = soup.select('.price-label')
        try:
            price = price[0].get_text()
        except:
            return 0
        price_int = 0
        for s in list(price):
            if s.isdigit():
                price_int =price_int * 10 + int(s)
        return price_int

    def get_features(self):
        response = self.__html_page
        soup = BeautifulSoup(response.text, 'html.parser')
        find = soup.find_all(class_='item')
        features1 = []
        for el in find:
            el = str(el)
            el = el.split('\n')
            for s in el:
                if s.find('<th>') == 0:
                    features1.append(self.cleanhtml(s))
        features2 = []
        find = soup.find_all(class_='value')
        for i in find:
            s = self.cleanhtml(str(i))
            s = s.replace(' ', '')
            s = s.replace('\t', '')
            s = s.replace('\n', '')
            features2.append(s)
        features = {}
        for i in range(0, len(features1)):
            features[features1[i]] = features2[i]
        return features

    def get_city(self):
        response = self.__html_page
        soup = BeautifulSoup(response.text, 'html.parser')
        find = soup.find_all(class_='show-map-link')
        return self.cleanhtml(find[0])

    def get_images(self):
        response = self.__html_page
        soup = BeautifulSoup(response.text, 'html.parser')
        # find = soup.find_all(class_= 'show-map-link')
        find = soup.find_all('img')
        images = []
        for i in find:
            s = str(i)
            if s.find('img alt') != -1 and s.find('nr') != -1:
                j = s.find('http')
                s = s[j:]
                s = s.replace('"/>', '')
                images.append(s)
        return images

    def get_date_time(self):
        response = self.__html_page
        soup = BeautifulSoup(response.text, 'html.parser')
        find = soup.find_all(class_='offer-titlebox__details')
        s = self.cleanhtml(find[0])
        s = s.replace('\n', '')
        i = s.find('La')
        s = s[i:]
        s = s.split(',')
        time = s[0].replace('La', '')
        time = time.replace(' ', '')
        date = s[1]
        date = date[1:]
        return time, date

    def get_add_number(self):
        response = self.__html_page
        soup = BeautifulSoup(response.text, 'html.parser')
        find = soup.find_all(class_='offer-titlebox__details')
        s = self.cleanhtml(find[0])
        s = s.replace('\n', '')
        i = s.find('La')
        s = s[i:]
        s = s.split(',')
        add_number = s[2]
        add_number = add_number[14:]
        return add_number
    def get_all(self):
        # method for getting a dict with all the information about an add
        dict = {'link': self.page_link, 'title': self.get_title(), 'description': self.get_description(),
          'price': self.get_price(), 'features': self.get_features(), 'city': self.get_city(),
          'images': self.get_images(), 'date, time': self.get_date_time(), 'add number': self.get_add_number()}
        return dict
    @staticmethod
    def cleanhtml(raw_html):
        raw_html = str(raw_html)
        cleantext = BeautifulSoup(raw_html, 'html.parser').text
        return cleantext

# This class is used to get multiple announcements links.
class olx_page:
    def __init__(self, link):
        self.page_link = link
        self.__html_page = requests.get(self.page_link)
    def get_ads_list(self):
        # Here we get all the ads on a specific page
        response = self.__html_page
        soup = BeautifulSoup(response.text, 'html.parser')
        find = soup.find_all(class_='marginright5 link linkWithHash detailsLink')
        link_list = []
        for s in find:
            link_list.append(self.__get_href(s))
        find = soup.find_all(class_='marginright5 link linkWithHash detailsLinkPromoted')
        for s in find:
            link_list.append(self.__get_href(s))
        return link_list
    def get_ads_for_x_pages(self,number_of_pages):
        # Here we take the array of pages created with get_pages_to method.
        pages_list = self.get_pages_to(number_of_pages)
        ads = []
        # For all those pages we create an olx_page object so that we can call the get_ads_list method.
        # ads array will be extended with arrays including ads of a specific page
        for page in pages_list:
            o_page = olx_page(page)
            ads.extend(o_page.get_ads_list())
        return ads
    def get_pages_to(self,j):
        # This method creates an array of links with '/?page='i' ' at the end.
        page_link = str(self.page_link)
        if 'page=' not in page_link:
            page_link += '?page=1'
        first_i = int(page_link[-1:])
        last_i = j
        pages = []
        for i in range(first_i, last_i):
            pages.append(page_link[:-1] + str(i))
        return pages
    def get_pages_number(self):
        # This method gets the number of available pages that can be scrapped for ads.
        response = self.__html_page
        soup = BeautifulSoup(response.text, 'html.parser')
        find = soup.find_all(class_='item fleft')
        find = find[len(find) - 1]
        find = str(find)
        find = find[::-1]
        page_number = ""
        for i in range(0, len(find)):
            if find[i].isdigit():
                page_number += find[i]
                if find[i + 1].isdigit():
                    page_number += find[i + 1]
                    if find[i + 2].isdigit():
                        page_number += find[i + 2]
                break
        return int(page_number[::-1])

    @staticmethod
    def __cleanhtml(raw_html):
        raw_html = str(raw_html)
        cleantext = BeautifulSoup(raw_html, 'html.parser').text
        return cleantext
    @staticmethod
    def __get_href(raw_html):
        # Getting a link with href tag from a string of raw_html
        raw_html = str(raw_html)
        link_with_html = BeautifulSoup(raw_html, 'html.parser')
        find = link_with_html.a["href"]
        return find