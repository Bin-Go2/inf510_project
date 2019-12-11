from django.shortcuts import render
from django.shortcuts import redirect
from . import models
from . import forms
import sqlite3
import json
import pandas as pd
from matplotlib import  pyplot as plt
import seaborn as sns

# Create your views here.


# this is a util function don't have url mapping
def transfer_chn_eng(city_list):
    '''


    :param list: [(name,flight_num)]
    :return: transfered list
    '''

    conn = sqlite3.connect('Flight.db')
    cursor = conn.cursor()
    sql_city = '''
                SELECT name_chn,name_eng
                FROM city
                LIMIT 20;
                '''
    city_info = cursor.execute(sql_city).fetchall()

    city_dict = {}

    for city in city_info:
        city_dict[city[0]] = city_dict.get(city[0],city[1]) # {'上海':'Shanghai'...}

    transfer_list = []

    if len(city_list[0]) ==2 : # cause i will use 2 types of list as parameters
        for city in city_list:
            city_eng = city_dict[city[0]]
            transfer_list.append((city_eng,city[1]))
    if len(city_list[0]) == 3:
        for city in city_list:
            city_eng1 = city_dict[city[0]]
            city_eng2 = city_dict[city[1]]
            transfer_list.append((city_eng1,city_eng2,city[2]))

    return transfer_list

def show_all(request):
    conn = sqlite3.connect('Flight.db')
    cursor = conn.cursor()

    sql_city = 'SELECT name_eng,longitude,latitude FROM city'
    city_info = cursor.execute(sql_city).fetchall()
    city_data = {}
    # get the city name and its location and as a context data
    for city in city_info:
        city_data[city[0]] = city_data.get(city[0],[city[1],city[2]])

    sql_flight = '''
                 SELECT departure_city,COUNT(*) AS counts
                 FROM flight
                 GROUP BY departure_city
                 ORDER BY counts DESC
                   '''

    result = cursor.execute(sql_flight).fetchall()
    transfer_result = transfer_chn_eng(result)

    city_and_num = [ {'name':i[0] , 'value': i[1]}  for i in transfer_result]

    # print(city_and_num)

    context = {
        'city_data':city_data,
        'data': city_and_num,
    }

    cursor.close()
    conn.close()

    return render(request, 'show_all_num.html',context)

def all_flights(request):

    conn = sqlite3.connect('Flight.db')
    cursor = conn.cursor()

    sql_city = 'SELECT name_eng,longitude,latitude FROM city'
    city_info = cursor.execute(sql_city).fetchall()
    city_data = {}
    # get the city name and its location and as a context data
    for city in city_info:
        city_data[city[0]] = city_data.get(city[0],[city[1],city[2]])

    sql_flight = '''
                    SELECT departure_city,COUNT(*) AS counts
                    FROM flight
                    GROUP BY departure_city
                    ORDER BY counts DESC
                      '''
    result = cursor.execute(sql_flight).fetchall()
    transfer_result = transfer_chn_eng(result)

    city_and_num = [{'name': i[0], 'value': i[1]} for i in transfer_result]

    context = {
        'data': city_and_num,
        'city_data':city_data,
    }

    cursor.close()
    conn.close()

    return render(request, 'all_flights.html',context)

def index(request):
    conn = sqlite3.connect('Flight.db')
    cursor = conn.cursor()

    sql_city = ' SELECT name_eng,longitude,latitude FROM city '
    city_info = cursor.execute(sql_city).fetchall()
    city_data = {}
    # get the city name and its location and as a context data
    for city in city_info:
        city_data[city[0]] = city_data.get(city[0], [city[1], city[2]])
    # format: ['Jiujiang': [116.00193, 29.705077], 'Zhuzhou': [113.133853, 27.827986]....]

    sql_flight = '''
                SELECT departure_city,COUNT(*) AS counts
                FROM flight
                WHERE date_time = '2019-12-25'
                GROUP BY departure_city
                ORDER BY counts DESC
                LIMIT 3 ;
                  '''
    result= cursor.execute(sql_flight).fetchall() #[('上海', 289), ('北京', 239), ('广州', 232)]
    transfer_result = transfer_chn_eng(result) # [('Shanghai', 289), ('Beijing', 239), ('Guangzhou', 232)]

    flight_list = [[],[],[]] # store the top3 city' flight

    for index,city_info in enumerate(result):
        city_name = city_info[0]
        sql_city = """
        SELECT departure_city, arrival_city,COUNT(*) AS count
        FROM flight
        WHERE date_time= '2019-12-25' AND departure_city = '{}'
        GROUP BY departure_city,arrival_city
                    """.format(city_name)

        arrival_result = cursor.execute(sql_city).fetchall()
        transfer_result = transfer_chn_eng(arrival_result)

        for i in transfer_result:
            flight_list[index].append(
                [
                    {'name':i[0]},
                    {'name':i[1],'value':i[2]}
                ]
            )

    context = {
        'city_data':city_data,
        'top_1':json.dumps(flight_list[0]),
        'top_2': json.dumps(flight_list[1]),
        'top_3': json.dumps(flight_list[2])

    }

    cursor.close()
    conn.close()

    return render(request, 'graphic.html', context)

def analysis(request):
    conn = sqlite3.connect('Flight.db')
    cursor = conn.cursor()

    sql_rank_population = 'SELECT name_chn, name_eng,rank,population FROM city ORDER BY rank LIMIT 20'

    result = cursor.execute(sql_rank_population).fetchall()

    city_name_chn = [i[0] for i in result][::-1]
    city_name = [i[1] for i in result][::-1]
    ranks = [i[2] for i in result][::-1]
    population = [ i[3] for i in result][::-1]

    # for index in range(len(population)):
    #     population[index] = population[index]/1000000

    sql_rank_flight_numbers = 'SELECT departure_city,COUNT(*) AS count FROM flight GROUP BY departure_city'
    flight_result = cursor.execute(sql_rank_flight_numbers).fetchall()


    flight_num = []
    for index,city in enumerate(city_name_chn):
        if_exist = False
        for j in flight_result:
            if j[0] == city:
                flight_num.append([city_name[index],j[1]])
                if_exist = True
        if  if_exist == False: # means there is no flight in that city
            flight_num.append([city_name[index], 0])

    flight = [i[1] for i in flight_num]

    # here I will use correlation analysis
    # between rank and flight_num , rank and population,flight_num and population
    df = pd.DataFrame({'GDP_rank':ranks,
                       'flight_num':flight,
                       'population':population
                       })

    corr = df.corr()

    gpd_related_flight = corr['GDP_rank']['flight_num']
    gpd_related_population = corr['GDP_rank']['population']
    flight_realted_population = corr['flight_num']['population']

    print(gpd_related_flight,gpd_related_population,flight_realted_population)

    context={
        'ranks':ranks,
        'city_name':city_name,
        'population':population,
        'flight_num':flight,

    }

    return render(request, 'analysis.html',context)

def statistic(request):
    conn = sqlite3.connect('Flight.db')
    cursor = conn.cursor()

    sql_rank_population = 'SELECT name_chn, name_eng,rank,population FROM city ORDER BY rank LIMIT 20'

    result = cursor.execute(sql_rank_population).fetchall()
    city_name_chn = [i[0] for i in result]
    city_name = [i[1] for i in result]
    ranks = [i[2] for i in result]
    population = [ i[3] for i in result]

    sql_rank_flight_numbers = 'SELECT departure_city,COUNT(*) AS count FROM flight GROUP BY departure_city'
    flight_result = cursor.execute(sql_rank_flight_numbers).fetchall()

    flight_num = []
    for index,city in enumerate(city_name_chn):
        if_exist = False
        for j in flight_result:
            if j[0] == city:
                flight_num.append([city_name[index],j[1]])
                if_exist = True
        if  if_exist == False: # means there is no flight in that city
            flight_num.append([city_name[index], 0])

    flight = [i[1] for i in flight_num]


    # here I will use correlation analysis
    # between rank and flight_num , rank and population,flight_num and population
    df = pd.DataFrame({'GDP_rank':ranks,
                       'flight_num':flight,
                       'population':population
                       })

    corr = df.corr()

    # result
    '''
                GDP_rank  flight_num  population
    GDP_rank    1.000000   -0.796007   -0.388563
    flight_num -0.796007    1.000000    0.349053
    population -0.388563    0.349053    1.000000

    '''

    gpd_gdp = corr['GDP_rank']['GDP_rank']
    fli_fli = corr['flight_num']['flight_num']
    pop_pop =  corr['population']['population']
    gpd_fli = corr['GDP_rank']['flight_num']
    gpd_pop = corr['GDP_rank']['population']
    fli_pop= corr['flight_num']['population']


    context={
        'gpd_gdp':gpd_gdp,
        'fli_fli':fli_fli,
        'pop_pop':pop_pop,
        'gpd_fli':gpd_fli,
        'gpd_pop':gpd_pop,
        'fli_pop':fli_pop


    }

    return render(request, 'statistic.html',context)


def register(request):
    if request.session.get('is_login', None):
        return redirect('/index/')

    if request.method == 'POST':
        register_form = forms.RegisterForm(request.POST)
        message = "Please check the input！"
        if register_form.is_valid():
            username = register_form.cleaned_data.get('username')
            password1 = register_form.cleaned_data.get('password1')
            password2 = register_form.cleaned_data.get('password2')

            if password1 != password2:
                message = 'Two input passwords must be consistent!'
                return render(request, 'register.html', locals())
            else:
                same_name_user = models.User.objects.filter(name=username)
                if same_name_user:
                    message = 'Account already exists!'
                    return render(request, 'register.html', locals())

                new_user = models.User()
                new_user.name = username
                new_user.password = password1
                new_user.save()

                return redirect('/login/')
        else:
            return render(request, 'register.html', locals())
    register_form = forms.RegisterForm()
    return render(request, 'register.html', locals())

def login(request):
    if request.session.get('is_login', None):  # check the status, if already login then go to the index page
        return redirect('/index/')

    if request.method == 'POST':
        login_form = forms.UserForm(request.POST)
        message = 'Please check the input！'
        if login_form.is_valid():
            username = login_form.cleaned_data.get('username')
            password = login_form.cleaned_data.get('password')

            try:
                user = models.User.objects.get(name=username) # retrieve the info from User table
            except:
                message = "Account doesn't exist!"
                return render(request, 'login.html', locals())

            if user.password == password:
                request.session['is_login'] = True
                request.session['user_id'] = user.id
                request.session['user_name'] = user.name
                return redirect('/index/')
            else:
                message = 'Wrong password！'
                return render(request, 'login.html', locals())
        else:
            return render(request, 'login.html', locals())

    login_form = forms.UserForm()
    return render(request, 'login.html', locals())

def logout(request):
    if not request.session.get('is_login', None):
        return redirect("/login/")
    request.session.flush()
    return redirect("/index/")