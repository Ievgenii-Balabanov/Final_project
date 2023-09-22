# Final_project
## Django Book Shop Quick Setup
### The current guide will help you set up the Django Shop project on your local computer.

#### Step #1: Install Dependencies
```bash
pip install -r requirements.txt
```

#### Step #2: Run the Development Server
```bash
python shop/manage.py runserver
```
#### Step #3: Apply Migrations
```bash
python shop/manage.py makemigrations
```
```bash
python shop/manage.py migrate
```
```bash
python shop/manage.py createsuperuser
```

#
#### Step 2: Run the Development Server
```bash
python warehouse/manage.py runserver 8001
```
#### Step 3: Apply Migrations
```bash
python warehouse/manage.py makemigrations
```
```bash
python warehouse/manage.py migrate
```
```bash
python warehouse/manage.py createsuperuser
```