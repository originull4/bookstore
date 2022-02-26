## Bookstore project using [Django](https://www.djangoproject.com/)

## Setting up the VirtualEnv and install dependencies
We will use [Virtualenv](https://pypi.org/project/virtualenv/) to setup the VirtualEnv.

```
git clone git@github.com:originull4/bookstore.git
cd bookstore
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Run the Application

```
python manage.py runserver
```

This will start the application on localhost and port 8000.
The server will start at <http://127.0.0.1:8000/>.

