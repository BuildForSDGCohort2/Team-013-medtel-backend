# Team-013-medtel-backend
# MEDTEL
Medtel is a Telemedicine system MVP that will help health professionals to check-up patients and extend their medical expertise to areas with less physicians. Also, this app will help patients access health specialists across different regions with no transportation time or costs.
This repository contains the code for the backend(API) of the system. 

Frontend repo: https://github.com/BuildForSDGCohort2/Team-013-medtel-frontend

## Getting Started

### Installing Dependencies

#### Python 3.7+

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by running:

```bash
pip3 install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) and [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/en/2.x/) are libraries to handle the lightweight sqlite database. 
- [jose](https://python-jose.readthedocs.io/en/latest/) JavaScript Object Signing and Encryption for JWTs. Useful for encoding, decoding, and verifying JWTS.

## Running the server

From within the `Team-013-medtel-backend` directory, first ensure you are working using your created virtual environment.

Each time you open a new terminal session, run:


```bash
export FLASK_APP=run.py 
export FLASK_ENV=development //To run the app in development mode 
```

## Endpoints
- BASE URL: **https://medtel-team-013.herokuapp.com/api/v1/**


**API Documentation** :https://documenter.getpostman.com/view/6911460/TVKD2chN
