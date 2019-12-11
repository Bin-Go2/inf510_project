import requests
import  sqlite3
from bs4 import BeautifulSoup
from retry import retry
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class City_scrape():

    """
    This is a scrapper about cities.
    It will retrieve top100 cities with largest GDP in China and store the data into sqlite database

    The data includes those attributes:
    id , city rank, city name in English , city name in Chinese,province,
    longitutude, latitude  and its population

    """

    def __init__(self,
                 city_url='https://www.chinacheckup.com/blogs/articles/china-city-economies',
                 personal_key='xxxx',
                 db='test.db',
                 open_chrome=True,
                 data_volume='all'):
        '''

        configurations  needed about scrape opreation
        :param city_url: the webpage that I have to scrape
        :param personal_key: google API key
        :param db: the connection db
        :param open_chrome: whether open the browser when using selenium
        '''

        self.city_url = city_url
        self.personal_key = personal_key  # google API key
        self.db = db  # dafault  'Flight.db '
        self.conn = sqlite3.connect(self.db) # default connection and cursor about db
        self.cursor = self.conn.cursor()
        self.data_volume = data_volume

        # open chrome browser and don't display
        self.open_chrome = open_chrome
        if self.open_chrome:
            chrome_options = Options()
            chrome_options.add_argument('--headless')
            self.driver = webdriver.Chrome('/usr/local/bin/chromedriver',options=chrome_options)
        else:
            self.driver = webdriver.Chrome('/usr/local/bin/chromedriver')
        self.create_table() # create the table to store information


    @retry(tries=50)  # here we use retry to catch exceptions and rerun again
    def population_scrape(self,city_name):
        '''
        Actually I nvaigate to another web page to crawl the population information
        because the original page doesn't  have this attribute

        :param city_name:
        :return: city's population in 2018
        '''
        driver = self.driver  # open chrome browser and don't display
        city_param = city_name + '人口'
        base_url = 'http://data.stats.gov.cn/search.htm?s='
        search_url = base_url + city_param
        # print(search_url)  http://data.stats.gov.cn/search.htm?s=上海人口
        driver.get(search_url)
        wait = WebDriverWait(driver, 10)
        wait.until(EC.presence_of_element_located((By.ID, "search_results")))
        wait.until(
            EC.presence_of_element_located(
                (By.XPATH, "//table//tr[2]//td[@align='right']")))
        # because if no results the default number is national population , so have to match the name
        city_verify = driver.find_element_by_xpath(
            "//table//tr[2]//td[@class='alignC'][1]")
        if city_verify.text == city_name:
            pop_ele = driver.find_element_by_xpath(
                "//table//tr[2]//td[@align='right']")
            population = int(float(pop_ele.text) * 10000)  # city's population
        else:
            population = 0  # which means there is no data in the national website
            # because some cities will not report the statistics to the government's website

        print(city_name, population)
        return population


    def create_table(self):
        conn = self.conn
        cursor = self.cursor
        sql_table = '''
                    create table if not exists city(
                    id integer primary key autoincrement,
                    rank integer,
                    name_eng varchar(40),
                    name_chn varchar(40),
                    province varchar(50),
                    longitude float,
                    latitude float,
                    population integer);
            '''
        cursor.execute(sql_table)
        conn.commit()

    def scrape_city_info(self):
        '''

        :return:  city_dictionary with key meaning rank and values meaning city info
        '''

        city_dictionary = {}
        response = requests.get(self.city_url)
        soup = BeautifulSoup(response.text, 'lxml')

        if self.data_volume == 'all':
            for each_row in soup.find_all(
                    'tr')[1:51]:  # top 100 GDP cities in China ; ~~ because 100 spend too much time
                columns = each_row.find_all('td')

                rank = columns[0].contents[0]
                name_eng = columns[1].contents[0]
                name_chn = columns[2].contents[0]
                province = columns[-1].contents[0]
                population = self.population_scrape(name_chn)

                # warp the request api
                req_api = "https://maps.googleapis.com/maps/api/geocode/json?address={}&key={}".format(
                    name_eng, self.personal_key)

                resp = requests.get(req_api)
                api_info = resp.json()   # transfer all the inforamtion of the city into json format
                latitude = api_info['results'][0]['geometry']['location']['lat']
                longitude = api_info['results'][0]['geometry']['location']['lng']

                city_dictionary[rank] = city_dictionary.get(
                    rank, [name_chn, name_eng, province, latitude, longitude,population])
                # print(city_dictionary)
                #each item in city_dictionary should like this
                # {'1': ['上海', 'Shanghai', 'Shanghai Municipality', 31.230416, 121.473701,24240000]}

        elif self.data_volume == 'sub':
            for each_row in soup.find_all(
                    'tr')[1:21]:  # top 20 GDP cities in China ; ~~ because 100 spend too much time
                columns = each_row.find_all('td')

                rank = columns[0].contents[0]
                name_eng = columns[1].contents[0]
                name_chn = columns[2].contents[0]
                province = columns[-1].contents[0]
                population = self.population_scrape(name_chn)

                # warp the request api
                req_api = "https://maps.googleapis.com/maps/api/geocode/json?address={}&key={}".format(
                    name_eng, self.personal_key)

                resp = requests.get(req_api)
                api_info = resp.json()  # transfer all the inforamtion of the city into json format
                latitude = api_info['results'][0]['geometry']['location']['lat']
                longitude = api_info['results'][0]['geometry']['location']['lng']

                city_dictionary[rank] = city_dictionary.get(
                    rank, [name_chn, name_eng, province, latitude, longitude, population])
                # print(city_dictionary)
                # each item in city_dictionary should like this
                # {'1': ['上海', 'Shanghai', 'Shanghai Municipality', 31.230416, 121.473701,24240000]}

        return city_dictionary

    def insert_to_tables(self):
        conn = self.conn
        cursor = self.cursor
        city_info = self.scrape_city_info()
        for key, values in city_info.items():
            rank = key
            name_chn, name_eng, province, latitude,longitude,population = values
            cursor.execute(
                        '''
                        insert into 
                        city (rank,name_eng,name_chn,province,longitude,latitude,population)
                        values (?,?,?,?,?,?,?)
                        ''',
                        (rank, name_eng, name_chn, province, longitude, latitude,population)
            )
            conn.commit()
        conn.close()


if __name__ == '__main__':

    url = 'https://www.chinacheckup.com/blogs/articles/china-city-economies'
    personal_key = '...'  # google API key
    test_instance = City_scrape(url,personal_key)
    test_instance.insert_to_tables()