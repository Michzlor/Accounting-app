### 1.Summary
A simple accounting app. Allows to change aacount balance, 
buy/sell item in inventory. App keeps track of all actions 
and saves action history, account value and inventory to local database.

## 2.Instalation
#### Requierments:
-Python version 3.9.13 or higher
#### Manual instalation:

1. Create directory for the application
2. Copy all files from the repository to directory You created
#### Instalation with Git:
In command line execute :
>git clone https://github.com/Michzlor/Accounting-app.git
It will create a directory named Accounting-app in your active directory(default: C/Users/username)
## 3.Start-up

1. Creating virtual environment
In command line execute
>  python -m venv env
2. Activating virtual environment
>  env/Scripts/activate
3. Instalation of packets and libraries used by app
> pip install -r requirements.txt
4. Initializing database
> flask db upgrade
5. Booting server for app. By default server runs on local host adress: http://127.0.0.1:5000
> flask run