# Horse Feed Planner

Course project for TKT20019 Databases and programming, autumn 2023

This project implements a web application for planning horse feeding. The application uses 
an SQL database to store and process data.


## Application features
The horse feed planner is an application that helps to optimize a diet of a horse.

User can save information about their horses and their feeding to their own user account. 
The application calculates the nutrients each horse receives and compares them to the recommendations. 
With this, the horse's owner can notice if the horse is getting too much or too little of a nutrient, 
and adjust the feeding accordingly.


## Information stored in the application's databases

### Horse information
The user can save a basic information for each horse, and what and how much it eats.
Information that affects the planning of horse feeding is e.g. the horse's age, type and 
condition, and how much it exercises.

### Feed information
The most important nutrients to consider when planning feeding are protein, minerals and vitamins. 
The energy content must also be taken into account.

The horse's most important feed is hay, which it must get enough of to keep its stomach healthy. 
Because the nutritional value of hay varies greatly, e.g. due to the weather, fertilizers and harvest time, 
the user can save in the application the information about the hay they use according to their current hay 
analysis results.

By default, the application's database contains the nutritional contents of some commonly used feeds, but the user can 
also add the feeds and supplements they use as needed.

### Feeding recommendations
The application contains the information of the horses' requirements tables for the most important nutrients. 
The application uses the official recommendations of the Natural Resources Institute Finland (Luke), which can 
be found at: https://maatalousinfo.luke.fi/fi/cms/rehu/hevoset/hevosten-ruokintasuositukset/

### User information
The app contains two kinds of users: normal users and adminstrators.
Normal users can save and modify information of their horses and feeds.
Administrators can remove user accounts and modify default feed information and feeding recommendations.


## The pages of the app
### Login page
- Fields to enter user name and password
- Not yet decided where and how the account creation is handled

### Main page
- List of user's horses containing links to their pages
- Link to "Add a new horse" page
- List of user's feeds
- Link to "Add a new feed" page
- Link to "All feeds" page

### Horse information page
- Horse's information in text fields, where they can also be modified
- A list of all the feeds the horse eats and how much nutrients it gets from each
- Summary of the nutrients the horse receives and the differences from the recommendations
- Buttons to ignore or save the changes

### Add a new horse page
- A form for entering the information on a new horse and its diet

### Feed information page
- The nutritional content of the feed
- The user can edit the information of the feeds they have added, but not the default feeds offered by the application.

### Add a new feed page
- A form for entering the information and nutritional content on a feed

### All feeds page
- On this summary page, information on the nutritional content of all stored feeds has been collected in one table.

### Administrator's page
- List of all the users and buttons to remove their accouts
- List of default feeds and forms to modify their contents
- Form to modify the feeding recommendations

## Status at 24.9.2023
### Already implemented:
- Regular users
- Account creation, login, logout
- Wiewing basic information on user's own horses
- Wiewing information on user's own and default feeds
- Possibility to add own horses into database
- Possibiity to add own feeds into database

### Remarks:
- The presentation and processing of feed information is still at an early stage. Entering feed information is difficult,
  as the program requires you to fill in all fields at this stage. The control of who has access to which feed's information is also incomplete.
- Adding the starting content of the database tables will be changed to be handled somehow other than copy-pasting.
- The code is very much a work in progress. The Pylint tool has not been used yet and there are no comments.
- The graphic design of the application is not final. The pages just have a touch of css to make them a little more pleasing to the eye.

## How to use the app

1. Go to the application directory

1. Start venv:
```source venv/bin/activate```

1. Install dependencies:
```pip install -r requirements.txt```

1. Create database tables:
```psql < schema.sql```

1. Start psql with command ```psql```
   
1. Give command ```\dt```. The database should contain tables feeds, horses, nutritions and users.

1. Copy-paste the contents of the file ```starter_content_for_the_database.txt``` into psql and press enter.

1. If you give commands
   ```SELECT * FROM nutrients;```
   and 
   ```SELECT name FROM feeds;```
you should see data in these tables.

1. Start the application with the command:
```flask run```

1. Start a browser and go to http://127.0.0.1:5000/ (or where Flask tells the app is running).

1. You can test creating an account and logging in, adding your own horses and feeds, and viewing their information.

