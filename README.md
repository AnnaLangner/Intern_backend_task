# Checking users project

  

It is a project in which we analyze user data.

  

## Contents

*  [General info](#genetal-info)

*  [Technologies](#technologies)

*  [Setup](#setup)

  

### General info

  

This project help you in easy way to pull up information about users in your data base.

  

Available commands:

* **python script/main.py percentage <female | male>** , returns percent of female or male in the database,

* **python script/main.py average-age [female | male]**, returns the average age of female or male, without a parameter, returns the average age of people in the database,

* **python script/main.py most-popular-cities --num=<N>**, returns the N most popular cities where users live,

* **python script/main.py most-common-passwords --num=<N>**, returns the N most used user paswords from the database.

* **python script/main.py users-born  --start-date=YYYY-MM-DD  --end-date=YYYY-MM-DD**, returns users born between start-date and end-date,

* **python script/main.py most-secure-password**, returns the most secure password from the database.

  

### Technologies

  

*Project is created with:*

* Python 3.7

* SQLite

  

### Setup