# Search Recipe Book
#### Video Demo:  <URL HERE>
#### Description:
If you have a large number of recipe books, you may not know which recipes are included in which books.
My family also had the above problem and solved it by entering the information into Excel and searching.
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

#### Configuration
Frontend: Bootstrap, HTML, jQuery  
Backend: flask  
ORM: SQLArchemy  
DB: SQLite3  
infrastructure: aws (maybe)  

#### setup dev
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
