# CineHoard
Check out movies from a wide variety of genres, add to your favorites, and build your watchlist.

## Setup
**These steps will set up project locally on you machine. To deploy it on heroku, read the instructions at the end.**  
Clone the project and install all the dependencies using:  
```python
pip install -r requirements.txt
```
Add your API_KEY in a private.py file in root directory of project.  
Now make migrations using:  
```python
python manage.py makemigrations
```
then apply migrations using:  
```python
python manage.py migrate
```
### Activating the cron job:  
Run following command to activate the cron job:  
```python
python manage.py crontab add
```
Now cron job will run after the interval specified in CRONJOBS in settings.py  

## Usage
Run 
```python
python manage.py add_movies
```
to add configured count (you can configure this count in constants.py file in movies directory) of movies.  
Run
```python
python manage.py runserver
```
to start the app.  

## Deployment on Heroku
Follow steps below to deploy the app on heroku:
- Make sure there's a file named `Procfile` in root directory._
- Run `pip install gunicorn`
- Your Procfile should have this line:
```
web: gunicorn cinehoard.wsgi
```
- Run pip install `psycopg2-binary`
- Create an app on heroku and add heroku remote to git:
```
heroku git:remote -a your-heroku-app-name
```
- Now commit all the changes and push to heroku:
```
git push heroku main
```
or 
```
git push heroku master
```
- Heroku will build the project and attach an ad-on of Postgresql to your app (Heroku doesn't support sqlite or any file based DB).
- Go to your app settings, you'll get DATABASE_URL in the config vars.
- Follow instructions here https://devcenter.heroku.com/articles/getting-started-with-python?singlepage=true#provision-a-database to set up the database.
- Once the database migrations are done, you'll be able to access the backend at your heroku app url.


## Running it Altogether
Once you have set up the backend, start the backend and frontend apps. Go to http://localhost:3000, you'll now have a working app.
