import os
from types import prepare_class
from selenium import webdriver
import json
import requests

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

class Hotels:

    def __init__(self):
        self.lst_title = []
        self.lst_ref = []
        self.category_flag = False
        self.dish_flag = False
        self.final_dict = []
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
        
        # driver.get(URL_TO_SCRAPE)
        # return
        proxy_pool = cycle(proxies)
        headers = {"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36"}
        
        i = 0
        s = requests.Session()
        for j in proxies:
        #Get a proxy from the pool
            proxy = next(proxy_pool)
            print("Request proxy: %s "%proxy)
            i += 1
            # os.system("export HTTP_PROXY=http://"+proxy)
            os.system("export HTTPS_PROXY=https://"+proxy)
        
            # export FTP_PROXY=proxy
            s.proxies = {"https": "https://"+proxy}
            r = s.get(URL_TO_SCRAPE, headers=headers, proxies={"http":"http://"+proxy, "https": "https://"+proxy})
            # r = requests.get(url,proxies={"http":"http://"+proxy, "https": "https://"+proxy})
            print(r.text)
            #     break
            # except:
            #     #Most free proxies will often get connection errors. You will have retry the entire request using another proxy to work. 
            #     #We will just skip retries as its beyond the scope of this tutorial and we are only downloading a single url 
            #     print("Skipping. Connnection error")
        # r = requests.get(URL_TO_SCRAPE)
        print(r)
        return
            



    #scrape the data of the given link
    def scrapData(self, URL_TO_SCRAPE=""):
        record = {}
        price = title = seller = phone = image = detail = location = category = sub_category = description = brand =None
        URL_TO_SCRAPE = 'https://www.ebay-kleinanzeigen.de/s-anzeige/apple-iphone-12-mini-128gb-weiss-neu/1838916714-173-21672'

        r = requests.get(self.get_scraperapi_url(URL_TO_SCRAPE))

        if r.status_code == 200:
        # with open('Apple iPhone 11 128 GB E buy cheap _ eBay.html', 'r') as f:
            html = r.text
            # html = f.read()
            
            soup = BeautifulSoup(html, 'lxml')

            phone_section = soup.select("#viewad-contact-phone")
            if phone_section:
                return None

            title_section = soup.select('#viewad-title')     
            if title_section:
                title = title_section[0].text.strip()

            price_section = soup.select('#viewad-price')
            if price_section:
                price = price_section[0].text.strip()
            

            seller_section = soup.select(".text-body-regular-strong text-force-linebreak")
            if seller_section:
                seller_name = seller_section[0].find_all('a')
                seller = seller_name[0].text.strip()
                # seller = selleer_section[0].select(".text-body-regular-strong text-force-linebreak")
                # seller = str(((seller[1].text).split("("))[0])
            

            
            category_section = soup.select(".breadcrump-link")
            if category_section:
                category_section
            

    
            image_section = soup.select('#viewad-image')
            if image_section:
                image = image_section[0]['src']


            location_section = soup.select("#viewad-locality")
            if location_section:
                location = location_section[0].text.strip()
        
            description_section = soup.select("#viewad-description-text")
            if description_section:
                description = description_section[0].text.strip()


            record = {
                'title': title,
                'price': price,
                "brand": brand,
                'seller': seller,
                'image': image,
                'description': description,
                'location': location,
                'phone': phone
            }

            if price == None or title == None or seller == None or image == None or  detail == None:
                return
            else:
                self.final_dict.append(record)




    # making list of links in self.lst_ref1566 of different products 
    def making_href_links_selenium(self, driver):

        page_count = 2
        pages_link = "https://www.ebay-kleinanzeigen.de/s-handy-telekom/seite:"+str(page_count)+"/c173"
        # driver.get('https://www.ebay-kleinanzeigen.de/s-handy-telekom/c173')
        driver.get(pages_link)
        # r = requests.get("https://www.ebay-kleinanzeigen.de/s-handy-telekom/c173")
        # print(r)
        # return
        time.sleep(2)
        elem1 = driver.find_element_by_xpath('/html/body/div[1]/div[2]/div/div[3]/div[2]/div[2]/div[2]')
        # print(elem1.text)
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
        return


    # making list of links in self.lst_ref1566 of different products 
    def making_href_links(self, driver):

        page_count = 2
        pages_link = "https://www.ebay-kleinanzeigen.de/s-handy-telekom/seite:"+str(page_count)+"/c173"
        
        # r = requests.get("https://www.ebay-kleinanzeigen.de/s-handy-telekom/c173")
        time.sleep(2)
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
    def persist_image(self, folder_path, url):
        try:
            # headers = {'User-agent': 'Chrome/64.0.3282.186'}
            image_content = requests.get(url).content
            
        except Exception as e:
            print(f"ERROR - Could not download {url} - {e}")    
        
        try:
            image_file = io.BytesIO(image_content)
            image = Image.open(image_file).convert('RGB')
            file_path = os.path.join(folder_path,hashlib.sha1(image_content).hexdigest()[:10] + '.jpg')
            with open(file_path, 'wb') as f:
                image.save(f, "JPEG", quality=85)
            print(f"SUCCESS - saved {url} - as {file_path}")
        except Exception as e:
            print(f"ERROR - Could not save {url} - {e}")
                

    def data_write(self):
        with open("mobile.json", "w") as outfile:
            json_object = json.dump(self.final_dict, outfile)

    def data_write_lst(self):
        with open('list_product_link.txt', 'w') as filehandle:
            for listitem in self.lst_ref:
                filehandle.write('%s\n' % listitem)
    

    def data_read_lst(self):
        r_lst_ref = []

        # open file and read the content in a list
        with open('listfile.txt', 'r') as filehandle:
            for line in filehandle:
                # remove linebreak which is the last character of the string
                currentPlace = line[:-1]

                # add item to the list
                r_lst_ref.append(currentPlace)


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
        

if __name__ == "__main__":

    
    

    # driver = webdriver.Firefox(executable_path="./geckodriver")
    
    instance = Hotels()

    # instance.broswer_open()
    instance.scrapData()
    # instance.making_href_links(driver=driver)
    
    # instance.data_write()
