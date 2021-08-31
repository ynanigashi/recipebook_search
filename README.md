Excel  
↓  
DB  
↓  
Search recipe

Frontend: Bootstrap, HTML, jQuery  
Backend: flask  
ORM: SQLArchemy  
DB: SQLite3  
infra: heroku | aws  

開発環境起動方法(Windows)
```
$env:SECRET_KEY = "hogehogehogehoge"
python app.py
````
DB初期化、検証ユーザ―作成
```
>>> from db import init_db
>>> init_db()
>>> from db import register_user
>>> register_user('<username>', '<password>')
```

memo
DB系の処理はdb.pyにまとめてapp.pyからは見えないようにする
