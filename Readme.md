# HM Compare

This program crawls the H&M website to find the price of each item and compare it over time. Also, finding the biggest sale prices for different items. 

To run the program on your own system, clone the git file and then create a virtual environment:

* on Windows:
`virtualenv hmscrapper_env`
`./hmscrapper_env/Scripts/activate`

* on Linux:
`virtualenv hmscrapper_env`
`source ./hmscrapper_env/bin/activate`

Then run the Django `manage.py` with:
`python manage.py makemigrations`
`python manage.py migrate`
`python manage.py runserver`

To run the program on Heroku, the complete instruction is available [here](https://devcenter.heroku.com/articles/getting-started-with-python)

You need to install Heroku first and then push the git repository to Heroku. 

To do that:
1. Create a heroku app with:
`heroku create hmscrapper`
2. Push the repository to the app:
`git push heroku master`
3. Open heroku app with either going [here](https://hmscrapper.herokuapp.com/)
or `heroku open`

To connect to the remote Heroku Postgres instance:

1. `heroku run bash`
2. `python manage.py migrate`

To run the app locally using Heroku:
1. Collect local assets:
`python manage.py collectstatic`

2. `heroku local web -f Procfile.windows`

3. Open http://localhost:5000 with your web browser.


Tutorial on how to use Postgre on Heroku and sqlite on Django local [here](https://medium.com/@BennettGarner/deploying-django-to-heroku-connecting-heroku-postgres-fcc960d290d1)

Unfortunately Heroku is blocked by H&M and in line 25 in views, where we want to parse information from the html file, response 403 occurs.

Remaining work:
1. Work on add-user feature to find if something is available in a particular size.

We have seen that using online proxies does not help to deroute the blocking of AWS ips.