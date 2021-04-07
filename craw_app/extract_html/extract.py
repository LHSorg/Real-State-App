#Libraries used
import requests
from bs4 import BeautifulSoup
import json
from requests import ConnectionError
import urllib3
import re 
import pandas as pd

class extract_text():
    def do_requests(self, url):
        try:
            headers = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.80 Safari/537.36'}
            response = requests.get(url, headers = headers)
            response.raise_for_status()
            return response.text
        except ConnectionError as e:
            print(f"Exception is {e}")
        else:
            return None   

    def get_links(self, soup_b):
        links = []
        links = [imovel.find_all('a')[1]['href'] for imovel in soup_b.find_all('div', class_ = 'col-12 col-lg-7 realty-details')]
        return links
    
    def get_text(self, html_extracted, data_complete):
        if not html_extracted:
            return None
        soup = BeautifulSoup(html_extracted, 'lxml')
        links = self.get_links(soup)
        
        for link in links:
            data = {}
            link = 'https://www.lelloimoveis.com.br' + link
            html = self.do_requests(link)
            soup = BeautifulSoup(html, 'lxml')
            getfeatures = soup.find('ul', class_ = 'list').find_all('li')
            getfeatures2 = soup.find('div', class_ = 'properties-container').find_all('p')
            
            for i in range(len(getfeatures)):
                # Initial simple cleaning
                clean_text = getfeatures[i].text.replace(' ', '').replace('\n', '')
                property_parts = re.sub(r'\([^)]*\)', '', clean_text)
                property_parts = re.findall('\d+|\D+', property_parts)
                data[property_parts[1]] = int(property_parts[0])

            for i in range(len(getfeatures2)):
                # Initial simple cleaning                
                clean_text = getfeatures2[i].text.replace(' ', '').replace('\n', '')                
                property_parts = re.sub(r'\([^)]*\)', '', clean_text)
                property_parts = re.findall('\d+|\D+', property_parts)
                if len(property_parts) > 1:
                    data[property_parts[1]] = int(property_parts[0])
                else:
                    data[property_parts[0]] = 1

            # Initial simple cleaning
            price = soup.find('div', class_ = 'row prices-row').find('p').text
            clean_text = price.replace(' ', '').replace('\n', '').replace('R$', '').replace('.', '').replace(',', '.').replace('\xa0', '')
            data['Price'] = float(clean_text)
            
            # Initial simple cleaning
            street = soup.find_all('div', class_ = 'card')[1].find('h1').find('small').text
            clean_text = street.replace('  ', '').replace('\n', '').replace('\xa0', '')
            data['Street'] = (clean_text)
            data_complete.append(data)
        return data_complete  
    
    def get_data(self, url, num):
        data_html = []
        for i in range(num):
            site_url = url + str(i + 1) + '-pagina'
            print(site_url)
            html_extract = self.do_requests(site_url)
            data_html = self.get_text(html_extract, data_html)

        df = pd.DataFrame(data_html)         
        with open("houses_extract.json", "w") as write_file:
            json.dump(df.to_dict(orient='index'), write_file, indent=8)
        write_file.close()

        return data_html










