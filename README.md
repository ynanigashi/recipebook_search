Excel  
↓  
DB  
↓  
Search recipe

Frontend: Bootstrap, HTML, jQuery  
Backend: flask  
ORM: SQLArchemy  
DB: SQLite3  
infrastructure: aws (maybe)  

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
