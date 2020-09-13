# django-delivery :package:

django-delivery is a backend service developed in Python using Django Framework. This project uses Graphql as the API to communicate with the frontend and
other client-side-apps. It uses Graphene-Django Library to build the Graphql API.
For authentication, JWT authentication is used.

## 1-Setup :wrench:

Create a virtual environement inside the project directory:

```bash
$ virtualenv venv

# Activate the virtual environment
$ source venv/bin/activate # for Linux
$ venv\Scripts\activate # for Windows
```
 ## Install requirements
 Use the package manager [pip](https://pip.pypa.io/en/stable/) to install the requirements of this project
```bash
$ pip install -r requirements.txt
```

## 2-Run Server

```bash
$ python manage.py runserver 8000
```
 Now open your browser on ```localhost:8000/graphql```, which is the only API endpoint.
 
 ### Try:
 
 ```
 {
  hello
 }
 ```
