# Horse Feed Planner

Course project for TKT20019 Databases and programming, autumn 2023

This project implements a web application for planning horse feeding. The application uses 
an SQL database to store and process data.

## Background of the project
Hay is the the most important part of a horse's diet as it provides essential fiber and nutrients, keeps the horse's digestive system healthy. In the wild, equine animals graze on grass almost continuously while also movin long distances and consuming a lot of energy.

Therefore the horse feeding should be based on the quality and quantity of hay. However, the nutritional value of hay varies greatly, e.g. due to the weather, fertilizers and harvest time, and affects what other feeding is necessary. A common issue with domesticated horses is that if they ate so much hay that they would get all the nutrients they need, they would often gain too much weight. That's why hay feeding usually has to be supplemented with other feeds and supplements.

The horse's individual characteristics, such as size, type and activity, affect the feeding it needs. Many horses also have health reasons, which is why, for example, the total amount of sugar in their feed is tried to be as low as possible, or the amount of fiber high.

## Limitations of the project
I had to draw a line on how precise I would make the Horse Feed Planner. For practical reasons, I had to leave out, for example, the special needs of young horses and pregnant mares, because the focus of the project seemed to shift too much to the side of Animal Science. Collecting nutritional recommendations was challenging, because foreign information is not completely valid in Finland due to, among other things, the shorter grazing season, less sunlight and different types of feeds and hay.

For those nutrients for which I could not find reliable minimum and maximum limits, I calculated the tolerances simply +- 10% of the recommendation. I also had to interpolate the recommendations of some nutrients for horses of different sizes.

I therefore tried to design the application in such a way that it can easily be expanded later.

## Application features
The horse feed planner is an application that helps to optimize a diet of a horse.

User can save information about their horses and their feeding to their own user account. 
The application calculates the nutrients each horse receives and compares them to the recommendations. 
With this, the horse's owner can notice if the horse is getting too much or too little of a nutrient, 
and adjust the feeding accordingly.

The application also contains default feeds added by administrators, which are available to all users.


## Information stored in the application's databases
The application contains the following database tables:

### users
The table "users" contains the application's user ID numbers, usernames, passwords in encrypted form and user role (basic or admin rights).

### horses
The table "horses" contains information of each horse, such as ID number, name, birth year, weight class, excercise level and owner. 

### feeds
The table "feed" contains the nutritional contents of different feeds for different nutrients. Each feed also has a reference to its owner, except for default feeds visible to all users, where the value of the owner field is 0.
The application has a few default feeds, which are added to the database before using the application, using the data.sql file after creating the database.

### nutritions
The table "nutritions" contains basic information for each nutrient. These include the nutrient name, abbreviation, unit, and a reference to which nutrient they are related to. The table also has a field so that in later versions of the application, additional information about the nutrient in question could be included.
This information is added to the database before using the application, using the data.sql file after creating the database.

### diets
The table "diets" contains information about the horses' diets by connecting the horses and the feeds they eat. It has fields for the amount of feed, and references to the horse and feed. These references are configured so that if the horse or feed in question is deleted from the database, the feedings contained in them are also removed.

### recommendations
The table "recommendations" contains recommended values and tolerances for different nutrients, sorted for horses of different sizes and with different activities.

Recommendations are also added to the database before using the application, using the data.sql file after creating the database.



## How to start using the app
1. Get project from github

1. Go to the application directory ```/horsefeedplanner/```

1. Create .env file with the following contents:

           DATABASE_URL="postgresql:///user"
           SECRET_KEY='key'
    - where user = your username
    - key = a random 16-character string enclosed within ''-marks

1. Create a Python virtual environment venv in the directory:
```python3 -m venv venv```

1. Start venv:
```source venv/bin/activate```

1. Install dependencies:
```pip install -r requirements.txt```

1. Create database tables:
```psql < schema.sql```

1. Insert the initial content into the database:
```psql < data.sql```

1. Start psql with command ```psql```
   
1. Give command ```\dt```. The database should contain tables feeds, horses, nutritions and users.

1. If you give commands
   ```SELECT * FROM nutritions;```
   and 
   ```SELECT name FROM feeds;```
you should see data in these tables.

1. For the first admin user, the role must be set manually from the command line to psql. 
This user can then give admin rights to other users.
   ```UPDATE users SET role = 'admin' WHERE id = <user's ID in database>;```

1. Start the application with the command:
```flask run```

1. Start a browser and go to http://127.0.0.1:5000/ (or where Flask tells the app is running).


## Using the app
### Register and login
- The start page has links to create a new user account or log in.

### Main page
- List of user's horses containing links to their pages
- Link to "Add a new horse" page
- List of user's feeds
- Link to "Add a new feed" page
- List of defaut feeds
- Admin users can choose whether the feeds they add are visible only to their own account, or whether they create default feeds that are visible to everyone.

### Horse information page
- Horse's basic information
- Horse's weight and activity, and inputs to update them
- A list of all the feeds the horse eats
- Inputs to add, remove and update horse's diet
- The Calcium/Phosphorus ratio of the horse's diet. This is one of the most important values to get right.
- List and amounts of nutrients whose needs and limits are very individual, but whose amounts are still useful to know.
- Complete summary of the nutrients the horse receives and the differences from the recommendations. 

### Add a new horse page
- A form for entering the information on a new horse and its diet

### Feed information page
- The nutritional content of the feed and link to modify it
- The user can edit the information of the feeds they have added, but basic user can not edit the default feeds offered by the application.
- Admin users can edit both their own and defaut feeds, but not other user's own feeds.

### Administrator's page
- List of all the users and buttons to update their user roles and remove their accouts
- Button to change own role to 'basic'
- Button to delete own user account


## Resources
Most of the nutrition info is from:
- Luke: Hevosten ruokintasuositukset, url: https://maatalousinfo.luke.fi/fi/cms/rehu/hevoset/hevosten-ruokintasuositukset/, referred: 6.10.2023
- Pirje Puumalainen: Hevosten vitamiiniruokinta, Savonia-ammattikorkeakoulu  9.5.2019, url: https://www.theseus.fi/handle/10024/168402, referred: 6.10.2023

The logo is created with Stable Diffusion Online (https://stablediffusionweb.com/) and then modified and turned into .svg with Gimp and Incscape. Footer image is drawn on base of the logo with the same programs.


