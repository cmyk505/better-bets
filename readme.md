## Better Bets - https://better-bets.herokuapp.com

**Gamble on NBA games with fake money**

Our app sources data for the current NBA season from [sportsdb](https://thesportsdb.com/), a free API. The home page displays upcoming NBA games, and, upon registering for an account, allocates users 500 play dollars to bet on events. An automated task checks every 10 minutes for updates to pending events.

### Technologies used

- Flask
- JavaScript
- Bootstrap
- Cypress

### To contribute

To get the app running locally, follow these steps:

1. After cloning the project, we recommend creating a virtual environment. Then, in the project directory, run

   > pip install -r requirements.txt

2. Create a free account with [sportsdb](https://thesportsdb.com/) to get an API key

3. Create a SQL database for use with the project locally

4. Next, set your environment variables by creating a .env file. At a minimum, set values for the following environment variables:

- SQLALCHEMY_DATABASE_URI
- FLASK_ENV
- API_KEY

1. In terminal, flask run

Note that locally, the application is using APScheduler, while in production it is using Heroku's native scheduling functionality. Any changes that use APScheduler should be isolated to the development environment by checking that app.config['FLASK_ENV'] = 'development'

### Add to our test suite

Our frontend is tested via Cypress, so to run the existing tests and contrbute, [install Cypress](https://docs.cypress.io/guides/getting-started/installing-cypress). **Alternatively**, you can run the tests in your terminal with Docker via the following command (run in the root directory of the project + replace $PWD as needed if you aren't using bash):

> docker run -it -v $PWD:/e2e -w /e2e cypress/included:3.2.0
