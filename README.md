Brew Ballot
===========

A simple application that allows you to set up a poll with some possible answers and let people text (SMS) in their votes using Twilio.

A web-based dashboard is also available to display the results as picture below.
![Dashboard Screenshot](/static/images/screenshot.png?raw=true "Dashboard Screenshot")

Setting Up
==========

Local Development
-----------------
1. Create the file brewballot/settings/secrets.json with the following contents filling in the blanks:


    {
      "SECRET_KEY": "",
      "TWILIO_ACCOUNT_SID": "",
      "TWILIO_AUTH_TOKEN": "",
      "VOTE_SMS_NUMBER": ""
    }
2. `./manage.py migrate` to migrate your database (sqlite by default in this case).
3. `./manage.py runserver` and point your browser to http://localhost:8000

Heroku
------
1. Push the code to Heroku
2. Add the following config vars with appropriate values:
  - SECRET_KEY
  - TWILIO_ACCOUNT_SID
  - TWILIO_AUTH_TOKEN
  - VOTE_SMS_NUMBER
3. View your Heroku app in a browser.