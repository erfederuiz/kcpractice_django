# Blog

How to install

clone project :

* git clone https://github.com/erfederuiz/kcpractice_django.git

After you have done with clone the repo.


Now you have to create a virtual environment

In your virtual environment you need to  install all the dependencies


Go to the project directory, and perform the following actions:

virtualenv .
pip3 install -r requirements.txt
chmod -R 777 .
bin/activate


Clean the database  (optional)
* python3 manage.py flush

Create a new admin user (optional)
* python3 manage.py createsuperuser



After Done with Installation, start the project.

* python3 manage.py runserver

