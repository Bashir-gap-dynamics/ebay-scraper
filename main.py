import os
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
        self.API_KEY = "5b050ad7666f81722e23933c08c69d2f"
        

    def get_scraperapi_url(self, url):
        """
            Converts url into API request for ScraperAPI.
        """
        payload = {'api_key': self.API_KEY, 'url': url}
        proxy_url = 'http://api.scraperapi.com/?' + urlencode(payload)
        return proxy_url


    #scrape the data of the given link
    def scrapData(self, URL_TO_SCRAPE):
        record = {}
        price = title = seller = phone = image = detail = location = None
    
        API_KEY = "5b050ad7666f81722e23933c08c69d2f"
    
        URL_TO_SCRAPE = 'https://www.ebay-kleinanzeigen.de/s-anzeige/apple-iphone-12-mini-128gb-weiss-neu/1838916714-173-21672'
    
        payload = {'api_key': API_KEY, 'url': URL_TO_SCRAPE, 'render': 'false'}
    
        r = requests.get('http://api.scraperapi.com', params=payload, timeout=60)
        # r = requests.get(URL_TO_SCRAPE)
        if r.status_code == 200:
        # with open('Apple iPhone 11 128 GB E buy cheap _ eBay.html', 'r') as f:
            html = r.text
            # html = f.read()
            soup = BeautifulSoup(html, 'lxml')
            title_section = soup.select('#viewad-title')     
            if title_section:
                title = title_section[0].text.strip()
            
    
            print(title)

            selleer_section = soup.select('#viewad-profile-box')
            print(selleer_section)
            return
            if selleer_section:
                # seller = selleer_section[0].text.replace('Sold by', '').replace('Positive feedbackContact seller', '')
                # selller = seller[:-6]
                phone = selleer_section[0].text.strip()
                # seller = selleer_section[0].select(".text-body-regular-strong text-force-linebreak")
                # seller = str(((seller[1].text).split("("))[0])
            

            print(phone)
            return

            price_section = soup.select('#viewad-price')
    
            if price_section:
                price = price_section[0].text
    
            image_section = soup.select('.vi-image-gallery__enlarge-link img')
    
            if image_section:
                image = image_section[0]['src']

            product_detail = soup.select("#ProductDetails")
            detail_dict = {}

            if product_detail:
                detail = product_detail[0]
                detail = detail.select(".spec-row")    
                for d in detail:
                    keys = d.find_all('div', {'class': 's-name'})
                    values = d.find_all('div', {'class': 's-value'})
                    count = 0
                    features_dict = {}
                    for k in keys:
                        features_dict[k.text] = values[count].text
                        count += 1
                    detail_dict[d.h2.text] = features_dict

            record = {
                'title': title,
                'price': price,
                'seller': seller,
                'image': image,
                'detail': detail_dict,
                'location': location
            }

            if price == None or title == None or seller == None or image == None or  detail == None:
                return
            else:
                self.final_dict.append(record)




    # making list of links in self.lst_ref1566 of different products 
    def making_href_links(self, driver):

        driver.get('https://www.ebay-kleinanzeigen.de/m-einloggen.html?targetUrl=/')
        time.sleep(15)
        # elem1 = driver.find_element_by_xpath("/html/body/div[1]/div[2]/div/section[1]/section/aside/div[2]/div/div/ul/li[2]/span")
        # print(elem1.text)
        return
        # li = elem1.find_elements_by_tag_name("a")
        # for i in li:
        #     self.lst_ref.append(i.get_attribute("href"))

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

    
    

    # driver = webdriver.Firefox(executable_path=r"D:\mehmood\Scraping Projects\restaurant_scrap\geckodriver-v0.29.1-win64\geckodriver.exe")
    
    instance = Hotels()
    instance.broswer_open()
    # instance.scrapData("https://www.ebay.com/p/5034585650?iid=202781903791")
    # instance.making_href_links(driver=driver)
    
    # instance.data_write()
