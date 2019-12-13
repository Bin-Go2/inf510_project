## INF510 Project description

### Here is a the final project for INF510. It is a project about data scraping and visualization.

This porject has two main parts:
1. data collecting: spider
2. visualization: FlightInfo

***

In the first part, I retrieve top 100 cities with largest GDP in China and scrape flight  informations between these citis a week before and after Christmas (12.22 - 12.28).And I collected the each city's population in 2018.Then I store these data into sqlite database as the database of django.


In the second part, I build a lightweight website by django, and by taking advantange of the data, I do some visualizations, such as
1. display all the flight numbers in different cities
2. display top3 cities which have the most flight numbers in Chrismtmas day.
3. make comparison among flight numbers, population,and  GDP among cities.
4. create a login/sign up part for the sake of future booking ticket system.

***

Here is how to run this project:

1.data collection:<br>
go to the project path `/inf510_project/src/scraper` 

then use command line
`python BIN_ZHANG_hw5.py -source=test`

`python BIN_ZHANG_hw5.py -source=remote`

`python BIN_ZHANG_hw5.py -source=local`


##### hint:  Cause I use the google api and when I published my project to Github, Github sent me a warning letter and ask me to delete it, so if you want to run these code, please add it in city_scarpe.py.
 
2.data visualization:<br>
2.1 go to the project path `/inf510_project/src/FlightInfo`
  
then use command line `python manage.py runserver`

2.2 go to the project path `/inf510_project` 

then use the command line  `jupyter notebook`

then open the notebook `zhang_bin.ipynb`

#### (Explanation)There is a little difference between my project paths and professor's requriment(cause my project needs to be located as the framework asked) . And I asked professor and got his permission. He asked me to explain it in the README and notebook.



Here is the visualization result:

![image](https://github.com/SondersB/inf510_project/blob/master/src/FlightInfo/airlines/static/img/1.png)
![image](https://github.com/SondersB/inf510_project/blob/master/src/FlightInfo/airlines/static/img/2.png)
![image](https://github.com/SondersB/inf510_project/blob/master/src/FlightInfo/airlines/static/img/3.png)
![image](https://github.com/SondersB/inf510_project/blob/master/src/FlightInfo/airlines/static/img/4.png)
![image](https://github.com/SondersB/inf510_project/blob/master/src/FlightInfo/airlines/static/img/5.png)
![image](https://github.com/SondersB/inf510_project/blob/master/src/FlightInfo/airlines/static/img/6.png)

