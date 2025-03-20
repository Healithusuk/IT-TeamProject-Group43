# README

### Requirements

This project is based on **Python 3.12.7**

Packages listed below should also be installed using **pip** before the application can run properly.

- Django 5.1.7
- bootstrap v5.3.0-alpha1
- mysqlclient 2.2.7
- pillow 11.1.0
- zxcvbn 4.5.0

# Secret File
In our development we use a secret file that is not uploaded to Github. It contains details (like username and password) of how we connect to database server, QQ SMTP server.
The file is called secrets.py and it looks like this:

```python
db_details = {
    'ENGINE': '',
    'NAME': '',
    'USER': '',
    'PASSWORD': '',
    'HOST': '',
    'PORT': '',
}
email_details={
    'EMAIL_BACKEND': '',
    'EMAIL_HOST': '',
    'EMAIL_PORT': ,
    'EMAIL_USE_TLS': ,
    'EMAIL_HOST_USER': '',
    'EMAIL_HOST_PASSWORD': '',
    'DEFAULT_FROM_EMAIL': '',
}
```

In order for our project to be executed and graded properly, we'll add secrets.py to the upload file. It will be in the directory ***Nifty/Nifty/***

If you are using completely different settings on db, or email, you can remove the call to secrets.py in settings.py and add your own settings.


# Database Connection Warning

We use a MySQL database on the DigitalOcean server. It is somehow **unavailable for on-campus network connection.** The solutions are:

1. Run the project from outside the campus, or
2. Use a hot spot if you have to run it on campus

# Access Control

We have two types of accounts, one account is an administrator account with permissions to manage the backend by accessing the backend page via the avatar drop-down box. 

The other account is a regular account that does not have access to the backend administration page.

Regular accounts can register on the site, and we provide an administrator account in the file "**username_password_for_admin**" for testing.
