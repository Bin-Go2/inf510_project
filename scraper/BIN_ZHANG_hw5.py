from city_scrape import *
from flight_scrape import *
import argparse
import  sqlite3

def get_data():
    conn = sqlite3.connect('test.db')
    cursor = conn.cursor()
    sql_city = 'SELECT * FROM city'
    sql_flight = 'SELECT * FROM flight'
    try:
        city_result = cursor.execute(sql_city).fetchall()
        flight_result = cursor.execute(sql_flight).fetchall()
        if len(city_result) == 0 :
            print('Please retrieve the data from remote webpage first.')
            print('You can use "python BIN_ZHANG_hw5.py -source=test" or ' ,end='')
            print('"python BIN_ZHANG_hw5.py -source=remote" to run.')
            return
    except:
        print('Please retrieve the data from remote webpage first.')
        print('You can use "python BIN_ZHANG_hw5.py -source=test" or ', end='')
        print('"python BIN_ZHANG_hw5.py -source=remote" to run.')
    else:
        print('=' * 80)
        for city in city_result:
            print(city)
        print('=' * 80)

        print('*' * 80)
        print('=' * 80)
        for flight in flight_result[:500]:
            print(flight)
        print('=' * 80)


def retrieve_sub_data():
    print('City information start collected(may take 0~1 minute)...')
    city_scrapper = City_scrape(data_volume='sub')
    city_scrapper.insert_to_tables()
    print('City information has been collected. Now collect flight information.')
    print('Flight information start collected(may take 5~6 minute)...')
    flight_scrapper = Flight_scrape(data_volume='sub')
    flight_scrapper.insert_to_tables()
    print('Flight information has been collected. Now get all the data. ')


def retrieve_all_data():
    print('City information start collected(may take 10+ minutes)...')
    city_scrapper = City_scrape()
    city_scrapper.insert_to_tables()
    print('City information has been collected. Now collect flight information.')
    print('Flight information start collected(may take 10+hours)...')
    flight_scrapper = Flight_scrape()
    flight_scrapper.insert_to_tables()
    print('Flight information has been collected. Now get all the data. ')


def test_fun():
    parser = argparse.ArgumentParser()
    parser.add_argument("-source", choices=["local",'remote','test'],help="where data should be gotten from")
    args = parser.parse_args()

    location = args.source

    if location == "test":
        # get data form remote webpage / scrape info for a small dataset
        retrieve_sub_data()
        get_data()
        
    elif location == "local":
        # get data form local database test.db
        get_data()

    else:
        # get data form remote webpage / scrape info for a small data set or large dataset
        data_range = int(input('Please input the data volume (0: subdata  1: alldata ):'))

        if data_range==0:
            retrieve_sub_data()
            get_data()

        if data_range ==1:
            retrieve_all_data()
            get_data()

if __name__ == '__main__':
    test_fun()

