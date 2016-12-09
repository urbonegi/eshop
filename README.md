# e-Shop Menu Application

e-Shop like Application managing Products and Categories tree menu for Python 3.5

Requires django 1.10 and psycopg2 libraries

## Getting started

### Running unit tests
Using tox basic dependencies are installed. Unit Tests uses in-memory DB.
 
```bash
pip install tox
tox -r
```

### Install application dependencies

```bash
pyvenv env
. env/bin/activate
pip install -r requirements_run.txt
```

### Setup postgres DB
Create eshop database and eshopuser. Assuming postgres DB on localhost. Modify database settings @ eshop/settings.py

```
CREATE DATABASE eshop;
CREATE USER eshopuser WITH PASSWORD 'password';
ALTER ROLE eshopuser SET client_encoding TO 'utf8';
ALTER ROLE eshopuser SET default_transaction_isolation TO 'read committed';
ALTER ROLE eshopuser SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE ehop TO eshopuser;
```

###Running migrations

```bash
python eshop/manage.py migrate
```

### Running stress test
Testing application performance when 10 000 active products added to the DB with many categories and subcategories

```bash
python eshop/manage.py stress_test
```

### Running unit test manually

```bash
python eshop/manage.py test --settings eshop.test_settings
```

### Create application superuser

```bash
python eshop/manage.py createsuperuser
```

### Running web application

```bash
python eshop/manage.py runserver
```

## Application Overview

Application specification doc is [here.](/task_spec.rst)
Application display Read-Only Menu of active Products and Categories @ index url. Under /admin site logged in users are allowed to add Categories and Products.

Additional behaviour assumptions done:
+ Model Validations added
    - Category can not be a parent for itself
    - Sub_categories can not be assigned to multiple categories
+ If product is inactive it is not shown in Read-Only Menu and not included to the 'active product count' (N)
+ DB is optimize to read data: Create and Delete new products and categories can take quite long time to optimise retrieve of data (db_index used)
+ Product can be added to different categories multiple times, then total product count adds it multiple times


