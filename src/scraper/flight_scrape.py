import sqlite3
import time
from lxml import etree
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from tqdm import tqdm
from retry import retry

class Flight_scrape():

    """
    This is a scrapper about flights information .
    It will retrieve data about Chinese city flights for one day
    Those city information comes from Flight db which collected by city_scrape class.
    And it will retrieve top 20 cities


    The flight data includes those attributes:
    id , flight_name, departure_city, arrival_city, departure_airport
    departure_time, arrival_airport, arrival_time, price,date_time
    """

    def __init__(self,
                 flight_url="https://www.ly.com/flights/home",
                 date_str='2019-12-22',
                 db='test.db',
                 data_volume='all'):

        self.db = db
        self.conn = sqlite3.connect(self.db)
        self.cursor = self.conn.cursor()
        self.flight_url = flight_url
        self.date_str = date_str # this date_str has a requirement which has to be  yyyy-mm-dd
        self.data_volume = data_volume

        chrome_options = Options()
        chrome_options.add_argument('--headless')
        self.driver = webdriver.Chrome('/usr/local/bin/chromedriver',options=chrome_options)  # open chrome browser
        self.scrape_error = {self.date_str:[]}
        self.create_table()

    def insert_to_tables(self):

        '''
        here are the retrieving operation to get all the flight info

        :return:
        '''

        # get the city's name and as the following departure place and arrival place
        cities_name = self.cursor.execute(
            "select name_chn from city ").fetchall()

        departure_city_list = [i[0] for i in cities_name][:20]
        arrival_city_list = departure_city_list

        if self.data_volume == 'all':
            # it will search for a long time because of selenium and time.sleep
            # here  I change it to one city instead of a city list
            # for departure_city in tqdm(departure_city_list,desc='1st loop',leave=True):
            for departure_city in tqdm(departure_city_list,desc='1st loop',leave=True):
                for arrival_city in tqdm(arrival_city_list,desc='2nd loop',leave=False):
                    if departure_city != arrival_city:
                        self.scrape_and_insert_info(departure_city, arrival_city,
                                                    self.date_str)
                print('{} has been scarped!'.format(departure_city))

            print('One day flight information from has been scraped!')

        elif self.data_volume == 'sub':
            # for departure_city in tqdm(departure_city_list,desc='1st loop',leave=True):
            for departure_city in tqdm(departure_city_list[0:2], desc='1st loop', leave=True):
                for arrival_city in tqdm(arrival_city_list, desc='2nd loop', leave=False):
                    if departure_city != arrival_city:
                        self.scrape_and_insert_info(departure_city, arrival_city,
                                                    self.date_str)
                print('{} has been scarped!'.format(departure_city))

            print('One day flight information from has been scraped!')


    @retry(tries=50) # set the max tries times if scraping failure
    def scrape_and_insert_info(self, departure_city, arrival_city, date):
        # request the base_url and operate the driver
        self.driver.get(self.flight_url)

        wait = WebDriverWait(self.driver, 10)
        wait.until(
            EC.presence_of_element_located((By.CLASS_NAME, "search-div")))

        wait.until(EC.presence_of_element_located((By.XPATH, "//input")))

        # set departure_place
        departure_place = self.driver.find_element_by_xpath(
            "//div[@class='search-div']/div[3]/div[1]/input")
        departure_place.clear()
        departure_place.send_keys(departure_city)  # departure terminal
        # set arrival_place
        arrival_place = self.driver.find_element_by_xpath(
            "//div[@class='search-div']/div[3]/div[3]/input")
        arrival_place.clear()
        arrival_place.send_keys(arrival_city)  # arrival terminal
        # set date_time
        date_time = self.driver.find_element_by_xpath(
            "//div[@class='search-div']/div[4]/div[1]/div[2]/input")
        date_time.clear()
        date_time.send_keys(date)
        search_btn = self.driver.find_element_by_xpath(
            "//button[@class='s-button']")
        search_btn.click()
        # self.driver.execute_script('arguments[0].click()',search_btn)

        text = self.driver.page_source
        tree = etree.HTML(text)
        flight_list = tree.xpath("//div[@class='flight-lists-container']/div")

        if len(flight_list) == 0:  # no flights
            time.sleep(1)
            # if no flight, we record the cities for manual checking
            # print("Can't retrieve the flight info from {} to {}".format(departure_city,arrival_city))

            # store the error  into scrape_error and after scraping collecting those flight again
            self.scrape_error[self.date_str].append([departure_city,arrival_city])
            return

        for each_flight in flight_list:
            # //div[@class='flight-lists-container']/div[1]//p[@class='flight-item-name']
            flight_name = each_flight.xpath(
                ".//p[@class='flight-item-name']/text()")[0]
            departure_time = each_flight.xpath(
                ".//div[@class='head-times-info']/div[1]/strong/text()")[0]
            departure_airport = each_flight.xpath(
                ".//div[@class='head-times-info']/div[1]/em/text()")[0]
            arrival_time = each_flight.xpath(
                ".//div[@class='head-times-info']/div[last()]/strong/text()"
            )[0]
            arrival_airport = each_flight.xpath(
                ".//div[@class='head-times-info']/div[last()]/em/text()")[0]
            price = int(
                each_flight.xpath(".//div[@class='head-prices']//em/text()")
                [0].replace('¥', ''))

            self.cursor.execute(
                '''
                    insert into flight
                    (flight_name,departure_airport,departure_city,arrival_city,
                    departure_time,arrival_airport,arrival_time,price,date_time)
                    values (?,?,?,?,?,?,?,?,?)''',
                (flight_name, departure_airport, departure_city, arrival_city,
                 departure_time, arrival_airport, arrival_time, price,date))

        self.conn.commit()

        # print('scraping {}--->{} complete'.format(departure_city, arrival_city))
        # Use a time gap 1s to avoid anti-scrape...')
        time.sleep(3)

    def create_table(self):
        sql_table = '''
            create table if not exists flight(
            id integer primary key autoincrement,
            flight_name varchar(60),
            departure_city varchar(60),
            arrival_city varchar(60),
            departure_airport varchar(50),
            departure_time varchar(40),
            arrival_airport varchar(50),
            arrival_time varchar(50),
            price integer,
            date_time varchar(50));
                    '''
        self.cursor.execute(sql_table)
        self.conn.commit()


if __name__ == '__main__':

    flight_url = "https://www.ly.com/flights/home"

    test_instance = Flight_scrape(flight_url, '2019-12-28')
    test_instance.insert_to_tables()

    # for a week flight scraping
    # test_instance = Flight_scrape(flight_url, '2019-12-22')
    # test_instance = Flight_scrape(flight_url, '2019-12-23')
    # test_instance = Flight_scrape(flight_url, '2019-12-24')
    # test_instance = Flight_scrape(flight_url, '2019-12-25')
    # test_instance = Flight_scrape(flight_url, '2019-12-26')
    # test_instance = Flight_scrape(flight_url, '2019-12-27')
    # test_instance = Flight_scrape(flight_url, '2019-12-28')