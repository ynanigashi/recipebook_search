# Recipe Book Search
#### Video Demo:  https://youtu.be/19AA544NBKQ
#### Description:
If you have a large number of recipe books, 
you may not know which recipes are included in which books.
My family also had the above problem and solved it 
by entering the information into Excel and searching.
So, I created a web application to make the search easier.

The features of this app are as follows
- User registration
- Password update
- Import information from Excel into the DB
- Search for recipes by ingredient
- Search for recipes from multiple ingredients
- Filter the search results by category
- Search for recipes by recipe name, author name, or book name
- Display a list of recipes by author
- Display a list of recipes in a book

Configuration of this app are as follows
Frontend: Bootstrap, HTML, jQuery  
Backend: flask  
ORM: SQLArchemy  
DB: SQLite3  
infrastructure: aws (maybe) 

How to use the application
The first step is to register users on the server side using commands.
Then, launch the web application and login. When the main screen appears after login, click on the "upload excel" icon on the left side of the navigation bar.
When the "Upload Excel" screen appears, select the Excel file you want to upload from the "Select File" menu. Once the file is uploaded, wait for the data to be registered in the database.
If the data has been successfully registered, a Flash message will be displayed to that effect. If the data is not registered successfully, there is a mistake in the file or the data you entered is incorrect.
(For example, the same material is registered in one line.
If the registration was successful, please perform a search. Click on the "Cook hat" link in the upper left corner to go to the search screen.

About the search screen
The search screen consists of two main forms, which can be switched between the "by ingredients" tab and the "by keyword" tab.

About the "by ingredients" tab
You can search for recipes by ingredients. The search results will include the name of the recipe, category, author, and book title. The search results will include the name of the recipe, the category, the author's name, and the title of the book. You can also filter the search results by category using the "filter by category" option.

When you enter text in the material input field, candidates will be displayed from among the materials registered in the DB. Clicking on a name will automatically perform a search on that material. Therefore, there is no search button. The search can also be performed on multiple ingredients. If you select more than one ingredient, the recipes that contain all of the ingredients will be displayed.

The "by keyword" tab
You can search for recipes by the name of the recipe, the author's name, or the title of the book. The search results will include the name of the recipe, the category, the author's name, and the title of the book.

Tip: You can get the results you want by entering the name of a dish, such as a salad, into the recipe search.

About search results
In the search results, the name of the recipe, the author's name, and the title of the book are links. Each of these will show you the following information
The name of the recipe: This will bring up the recipe details screen, which will show the ingredients needed in addition to what was shown in the search results.
Author's name: A list of recipes by the same author will be displayed.
Book title: A list of recipes contained in the book will be displayed.

How to start the development environment(Windows powershell)
```
Add-type -AssemblyName System.Web
$env:SECRET_KEY = [System.Web.Security.Membership]::GeneratePassword(16, 3)
python app.py
````

db initiarize and register user
```
>>> from db import init_db
>>> init_db()
>>> from db import register_user
>>> register_user('<username>', '<password>')
```
