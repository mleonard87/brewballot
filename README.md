Brew Ballot
===========

A simple application that allows you to set up a poll with some possible answers and let people text (SMS) in their votes using Twilio.

A web-based dashboard is also available to display the results as picture below.
![Dashboard Screenshot](/../screenshots/dashboard.png?raw=true "Dashboard Screenshot")

The home page will take you to the dashboard for the currently active poll if there is one, otherwise it will display "No Active Polls".

To view a list of all polls go to /all in the URL. (e.g. http://localhost:8000/all)

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
3. `./manage.py runserver` and point your browser to http://localhost:8000 to view the dashboard.

Heroku
------
1. Push the code to Heroku
2. Add the following config vars with appropriate values:
  - SECRET_KEY
  - TWILIO_ACCOUNT_SID
  - TWILIO_AUTH_TOKEN
  - VOTE_SMS_NUMBER
3. View your Heroku app in a browser to visit th dashboard.

Configuration
=============

The configuration of the polls is carried out using Django admin at http://localhost:8000/admin

SMS Options
===========
- POLLHELP - Get a response containing the currently active poll question and the list of possible answers.
- RESULTS - Get a response containing the currently active poll question and each of the answers with their current scores.
- UNVOTE - Remove your vote from the currently active poll if you have already voted.
- Option (e.g. Mike) - The name of the one of the possible poll options to vote for that option. If you have already voted you vote will be changed - you cannot vote twice.
