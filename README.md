## INF510 Project desription

### Here is a the final project for INF510. It is a project about web scraping and django.

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
go to the project path `/inf510_project/src/scraper`  and use command line <br>
`python BIN_ZHANG_hw5.py -source=remote`
`python BIN_ZHANG_hw5.py -source=local`
`python BIN_ZHANG_hw5.py -source=test`

##### hint:  Cause I use the google api and when I published my project to Github, Github sent me a warning letter and ask me to delete it, so if you want to run these code, please add your own google api key or use my homework5's project. 
 
2.data visualization:<br>
(1) go to the project path `/inf510_project/src/FlightInfo`  and use command line <br>
`python manage.py runserver`

(2) go to the project path `/inf510_project` and use the command line <br>
`jupyter notebook`
then open the notebook 'zhang_bin.ipynb' 
