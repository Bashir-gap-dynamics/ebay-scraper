import os
from types import prepare_class
from selenium import webdriver
import json
import requests
from pprint import pprint
from bs4 import BeautifulSoup
try:
    from PIL import Image
except ImportError:
    import Image

# from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
# from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
import time
import datetime

from itertools import cycle
import traceback
from lxml.html import fromstring

import hashlib

import io
try:
    from urllib import urlencode
except ImportError:
    from urllib.parse import urlencode

class VERIFIEDDATA:

    def __init__(self):
        self.lst_ref_numbered = []
        self.lst_ref = []
        self.final_dict = {}
        self.unverified_data = {}
        self.verified_data = {}
        self.lst_phone = []
        self.lst_ref_with_phone = {}
        self.API_KEY = "9f91386be094fb6308102d580a01381c"


    
    def get_proxies(self):
        url = 'https://free-proxy-list.net/'
        response = requests.get(url)
        parser = BeautifulSoup(response.text, 'lxml')
        proxies = []
        elem = parser.select('#proxylisttable')
        keys = elem[0].find_all('tr')
        keys = keys[1:]
        for i in keys:
            td=i.find_all("td")
            try:
                if td[6].text == "yes":
                    # print(td[0].text, td[1].text)
                    proxies.append(td[0].text+":"+td[1].text)
            except:
                continue
        # print(proxies)
        return proxies
        

    def get_scraperapi_url(self, url):
        """
            Converts url into API request for ScraperAPI.
        """
        payload = {'api_key': self.API_KEY, 'url': url}
        proxy_url = 'http://api.scraperapi.com/?' + urlencode(payload)

        return proxy_url


    
    def scrapDataSelenium(self, driver, URL_TO_SCRAPE=""):

        price = title = seller = phone = image = detail = location = category = sub_category = description = brand = None
    
        URL_TO_SCRAPE = 'https://www.ebay-kleinanzeigen.de/s-anzeige/apple-iphone-12-mini-128gb-weiss-neu/1838916714-173-21672'
        
        driver.get(URL_TO_SCRAPE)
        time.sleep(5)
        try:
            elem1 = driver.find_element_by_xpath("/html/body/div[2]/div/div[1]/div/a")
            elem1.click()
            time.sleep(2)
            print("hello")
            elem1 = driver.find_element_by_xpath("/html/body/div[1]/div[2]/div/section[1]/section/aside/div[2]/div/div/ul/li[2]/span/span[1]")
            print("number", elem1.text)
            elem1 = driver.find_element_by_xpath("/html/body/div[1]/div[2]/div/section[1]/section/section/article/div[1]/div[1]/img")
            image = elem1.get_attribute("src")
            print(image)
            elem2 = driver.find_element_by_xpath("/html/body/div[1]/div[2]/div/section[1]/section/section/article/div[3]/h1/span[2]")
            title = elem2.text
            print(title)
            elem3 = driver.find_element_by_xpath("/html/body/div[1]/div[2]/div/section[1]/section/section/article/div[3]/h2")
            price = elem3.text
            print(price)
            elem4 = driver.find_element_by_xpath("/html/body/div[1]/div[2]/div/section[1]/section/section/article/div[3]/div/div[1]/span")
            location = elem4.text
            print(location)
            elem5 = driver.find_element_by_xpath("/html/body/div[1]/div[2]/div/section[1]/section/aside/div[2]/div/div/ul/li[1]/span/span[1]/a")
            seller = elem5.text
            print(seller)
            elem6 = driver.find_element_by_xpath("/html/body/div[1]/div[2]/div/div[3]/div/a[3]/span")
            sub_category = elem6.text
            print(sub_category)
            elem7 = driver.find_element_by_xpath("/html/body/div[1]/div[2]/div/div[3]/div/a[2]/span")
            category = elem7.text
            print(category)
            elem8 = driver.find_element_by_xpath("/html/body/div[1]/div[2]/div/section[1]/section/section/article/div[6]/div/p")
            description = elem8.text
            print(description)
            elem9 = driver.find_element_by_xpath("/html/body/div[1]/div[2]/div/section[1]/section/section/article/div[5]/ul/li[1]/span")
            brand = elem9.text
            print(brand)
        except:
            print("cool")
            # continue

    
    #scrape the data of the given link
    def scrapDataRotatingIps(self, URL_TO_SCRAPE=""):
        record = {}
        price = title = seller = phone = image = detail = location = category = sub_category = description = brand =None
    
        URL_TO_SCRAPE = 'https://www.ebay-kleinanzeigen.de/s-anzeige/apple-iphone-12-mini-128gb-weiss-neu/1838916714-173-21672'
        
        proxies = self.get_proxies()
        print(proxies)
        
        proxy_pool = cycle(proxies)
        headers = {"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36"}
        
        i = 0
        s = requests.Session()
        for j in proxies:
        #Get a proxy from the pool
            proxy = next(proxy_pool)
            print("Request proxy: %s "%proxy)
            i += 1
            os.system("export HTTP_PROXY=http://"+proxy)
            os.system("export HTTPS_PROXY=https://"+proxy)
        
            # export FTP_PROXY=proxy
            s.proxies = {"https": "https://"+proxy}
            r = s.get(URL_TO_SCRAPE, headers=headers, proxies={"http":"http://"+proxy, "https": "https://"+proxy})
            try:
                print(r.text)
                break
            except:
                #Most free proxies will often get connection errors. You will have retry the entire request using another proxy to work. 
                #We will just skip retries as its beyond the scope of this tutorial and we are only downloading a single url 
                print("Skipping. Connnection error")
        return
            



    #scrape the data of the given link
    def scrapData(self, URL_TO_SCRAPE=""):
        record = {}
        price = title = seller = phone = image = detail = location = category = sub_category = description = brand = date = detail = None
        URL_TO_SCRAPE = 'https://www.ebay-kleinanzeigen.de/s-anzeige/apple-iphone-12-mini-128gb-weiss-neu/1838916714-173-21672'

        r = requests.get(self.get_scraperapi_url(URL_TO_SCRAPE))

        if r.status_code == 200:
            html = r.text
            soup = BeautifulSoup(html, 'lxml')
            
            phone_section = soup.select("#viewad-contact-phone")
            if not phone_section:
                return None
            
            title_section = soup.select('#viewad-title')     
            if title_section:
                title = title_section[0].text.strip()
            
            price_section = soup.select('#viewad-price')
            if price_section:
                price = price_section[0].text.strip()
            

            seller_section = soup.select("#viewad-contact")
            if seller_section:
                seller_name = seller_section[0].find_all('a')
                seller = seller_name[1].text.strip()
            

            
            category_section = soup.select(".breadcrump-link")    
            if category_section:
                category_section_1 = category_section[1].find_all("span")
                category = category_section_1[0].text

                category_section_2 = category_section[2].find_all("span")
                sub_category = category_section_2[0].text

    
            image_section = soup.select('#viewad-image')
            if image_section:
                image = image_section[0]['src']


            location_section = soup.select("#viewad-locality")
            if location_section:
                location = location_section[0].text.strip()
        
            description_section = soup.select("#viewad-description-text")
            if description_section:
                description = description_section[0].text.strip()

            date_section = soup.select("#viewad-extra-info")
            if date_section:
                dated = date_section[0].find_all("span")
                date = dated[0].text.strip()


            brand_section = soup.select(".addetailslist")
            if brand_section:
                detail_section_1 = brand_section[0].find_all("li")
                detail_count = 0
                for k in detail_section_1:
                    if detail_count == 0:
                        temp = k.text.strip()
                        temp = temp.split("\n")
                        detail = temp[0].strip()
                        detail += " : "+temp[1].strip() + "\n"
                        brand= temp[1].strip()
                        detail_count += 1
                        continue

                    temp = k.text.strip()
                    temp = temp.split("\n")
                    detail += temp[0].strip()
                    detail += " : "+temp[1].strip() + "\n" 
                    detail_count += 1


            record = {
                "seller":{
                    "seller_name": seller,
                    "seller_email": seller+"@gmail.com",
                    "password": seller+"1234@gap", 
                    "store_name":seller+"-store",
                    "store_email":seller+"-store@gmail.com",
                    "state":None,
                    "location":location,
                    "city": (location.split("-"))[-1].strip(),
                    "phone":phone,
                    "country": "Germany"
                    },
                "product":[{
                    'title': title,
                    'price': price,
                    "brand": brand,
                    "category":category,
                    "sub_category": sub_category,
                    'seller': seller,
                    'image': image,
                    "date":date,
                    "detail": detail,
                    'description': description,
                    'location': location,
                    'phone': phone
                }]
            }

            return record
            # pprint(record)
        return None
        




    # making list of links in self.lst_ref1566 of different products 
    def making_href_links_selenium(self, driver):

        page_count = 2
        pages_link = "https://www.ebay-kleinanzeigen.de/s-handy-telekom/seite:"+str(page_count)+"/c173"
        
        driver.get(pages_link)
        time.sleep(2)
        elem1 = driver.find_element_by_xpath('/html/body/div[1]/div[2]/div/div[3]/div[2]/div[2]/div[2]')
        
        li = elem1.find_elements_by_tag_name("a")
        for i in li:
            self.lst_ref.append(i.get_attribute("href"))
        
        time.sleep(3)

        page_count += 1
        while (page_count < 10):
            driver.get("https://www.ebay-kleinanzeigen.de/s-handy-telekom/seite:"+str(page_count)+"/c173")
            time.sleep(2)
            elem1 = driver.find_element_by_xpath('/html/body/div[1]/div[2]/div/div[3]/div[2]/div[2]/div[2]')
            # print(elem1.text)
            li = elem1.find_elements_by_tag_name("a")
            for i in li:
                self.lst_ref.append(i.get_attribute("href"))
            
            time.sleep(3)
            page_count += 1

        print(self.lst_ref)
        self.data_write_lst()
        self.data_write()
        return


    # making list of links in self.lst_ref1566 of different products 
    def making_href_links(self):

        page_count = 2
        # pages_link = "https://www.ebay-kleinanzeigen.de/s-handy-telekom/seite:"+str(page_count)+"/c173"
        
        r = requests.get(self.get_scraperapi_url("https://www.ebay-kleinanzeigen.de/s-handy-telekom/c173"))
        if r.status_code == 200:
            html = r.text
            soup = BeautifulSoup(html, 'lxml')
            product_section = soup.select("#srchrslt-adtable")
            if product_section:
                product_links = product_section[0].find_all("a")
                for j in product_links:
                    self.lst_ref.append("https://www.ebay-kleinanzeigen.de"+j['href'])
        
        while (page_count < 0):
            r = requests.get(self.get_scraperapi_url("https://www.ebay-kleinanzeigen.de/s-handy-telekom/seite:"+str(page_count)+"/c173"))
            if r.status_code == 200:
                html = r.text
                soup = BeautifulSoup(html, 'lxml')
                product_section = soup.select("#srchrslt-adtable")
                if product_section:
                    product_links = product_section[0].find_all("a")
                    for j in product_links:
                        self.lst_ref.append("https://www.ebay-kleinanzeigen.de"+j['href'])
            page_count += 1

        counter = 0
        for i in self.lst_ref:
            print(i)
            data = self.scrapData(i)
            if data == "None":
                continue
            self.final_dict[i] = data
            self.lst_ref_numbered.append(i)
            if counter == 10:
                break
            counter += 1
        self.data_write_lst()
        self.data_write()
        
        return




    def creating_file_structure(self):
        count = 0
        for j in self.lst_ref:
            print(j)
            self.scrapData(j) 

        for k in self.final_dict:
            if k["image"] != None:
                path = "./Sellers"
                current_seller = [name for name in os.listdir(path) if os.path.isdir(name)]
                print(current_seller)
                seller_folder = k["seller"]
                product_folder = k["title"]
                print(seller_folder)
                print(product_folder) 
                
                
                print("go")
                if seller_folder not in current_seller:
                    seller_path = os.path.join(path, seller_folder)
                    try:
                        os.mkdir(seller_path)
                    except:
                        product_path = os.path.join(seller_path, product_folder)
                        try:
                            os.mkdir(product_path)
                            self.persist_image(product_path, k["image"])
                            with open(product_path+'/data.json', 'w') as fp:
                                json.dump(k, fp)
                        except:
                            continue 
                    
                else:
                    seller_path = os.path.join("./Sellers", seller_folder)
                    product_path = os.path.join(seller_path, product_folder)
                    
                    self.persist_image(product_path, k["image"])
                    with open(product_path+'/data.json', 'w') as fp:
                        json.dump(k, fp)
                    



    # getting images saved into folder ./images 
    def persist_image(self, url):
        try:
            # headers = {'User-agent': 'Chrome/64.0.3282.186'}
            image_content = requests.get(url).content
            
        except Exception as e:
            print(f"ERROR - Could not download {url} - {e}")    
        
        try:
            image_file = io.BytesIO(image_content)
            image = Image.open(image_file).convert('RGB')
            file_path = os.path.join("./images",hashlib.sha1(image_content).hexdigest()[:10] + '.jpg')
            with open(file_path, 'wb') as f:
                image.save(f, "JPEG", quality=85)
            print(f"SUCCESS - saved {url} - as {file_path}")
            return file_path
        except Exception as e:
            print(f"ERROR - Could not save {url} - {e}")
            return None
                

    def data_write(self):
        with open("data_unverified.json", "w") as outfile:
            json_object = json.dump(self.final_dict, outfile)
    
    def data_write_verified(self):
        with open("data_verified.json", "w") as outfile:
            json_object = json.dump(self.verified_data, outfile)

    def data_write_lst(self):
        with open('list_product_link.txt', 'w') as filehandle:
            for listitem in self.lst_ref_numbered:
                filehandle.write('%s\n' % listitem)
    

    def data_write_lst_phone_number(self):
        with open('phone_numbers.txt', 'w') as filehandle:
            for listitem in self.lst_phone:
                filehandle.write('%s\n' % listitem)
    

    def data_read_phone(self):
        
        # open file and read the content in a list
        with open('phone_numbers.txt', 'r') as filehandle:
            for line in filehandle:
                # remove linebreak which is the last character of the string
                currentPlace = line[:-1]

                # add item to the list
                self.lst_phone.append(currentPlace)
        

    
    def data_read_ref_with_phone(self):
        
        # open file and read the content in a list
        with open('url_number.txt', 'r') as filehandle:
            for line in filehandle:
                # remove linebreak which is the last character of the string
                currentPlace = line[:-1]

                # add item to the list
                lst = currentPlace.split(",")
                self.lst_ref_with_phone[lst[0]] = lst[1]
        



    def read_data_verified(self):    
        # Opening JSON file
        f = open('data_verified.json',)
        
        self.verified_data = json.load(f)
        
        # Closing file
        f.close()


    def read_data_unverified(self):    
        # Opening JSON file
        f = open('data_unverified.json',)
        
        self.unverified_data = json.load(f)
        
        # Closing file
        f.close()


    def broswer_open(self):
        import webbrowser

        url = 'https://www.ebay-kleinanzeigen.de/s-anzeige/apple-iphone-12-mini-128gb-weiss-neu/1838916714-173-21672'

        # MacOS
        # chrome_path = 'open -a /Applications/Google\ Chrome.app %s'

        # Windows
        # chrome_path = 'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s'

        # Linux
        chrome_path = '/usr/bin/google-chrome %s'

        webbrowser.get(chrome_path).open(url)
        time.sleep(4)
        webbrowser.open(url)


    def main(self):
        self.data_read_ref_with_phone()
        self.data_read_phone()
        self.read_data_unverified()
        self.read_data_verified()
        # print(self.verified_data)
        # print(self.unverified_data)
        # print(self.lst_phone)
        # print(self.lst_ref_with_phone)
        for k,v in self.lst_ref_with_phone.items():
            if v in self.lst_phone:
                product = self.unverified_data[k]["product"][0]
                product["phone"] = v
                product["image"] = self.persist_image(product["image"])
                self.verified_data[v]["product"].append(product)
            else:
                try:
                    
                    self.unverified_data[k]["seller"]["phone"] = v
                    self.unverified_data[k]["product"][0]["phone"] = v
                    self.unverified_data[k]["product"][0]["image"] = self.persist_image(self.unverified_data[k]["product"][0]["image"])
                    self.verified_data[v] = self.unverified_data[k]
                    pprint(self.verified_data)
                    self.lst_phone.append(v)
                except:
                    continue
        
        self.data_write_verified()
        self.data_write_lst_phone_number()


        
if __name__ == "__main__":

    
    

    # driver = webdriver.Firefox(executable_path="./geckodriver")
    
    instance = VERIFIEDDATA()
    instance.main()
    # instance.data_