# scraping part


1.retrieve top100 cities with largest GDP in China and store the data into sqlite database (100 records)</br>
2.retrieve flight information in the Christmas week among all the cities according to the data from 1 (1.4w+ records)


If you want to run these code, please make sure you have downloaded all the libraries:
#### requests、beautifulsoup4、retry、selenium、lxml、tqdm

####  And in city_scrape.py , Google API is needed, for the sake of publiccation, when you run the code, please use your own google API.

Here is another configuration need to be set up: chromedriver which in #48,#50 in city_scrape.py and #40 in flight_scrape.pyso this chromedriver has to be downloaded first and be set in the proper location and then selenium can use it.

Mac's path is like:
#### /usr/local/Username/chromedriver</br>
Windows's path is like
#### C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe

 (BTW, if any abnormal output on the command line, that could be the driver's problem but it doesn't influence the function normally operating.)








