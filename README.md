# DRF-Ecommerce

## Description

**DRF-Ecommerce is a Django project designed to revolutionize the online shopping experience, offering an expansive platform tailored for e-commerce functionalities. Our project encapsulates a myriad of features essential to modern e-commerce platforms, mirroring the seamless transactions and interactive interfaces of leading online marketplaces.**

## Features

- User Authentication
- Products
- Categories



### Technologies Used

| Python | Django | Rest Framework | SQLite |
|--------|--------|----------------|--------|
| <img src="https://upload.wikimedia.org/wikipedia/commons/c/c3/Python-logo-notext.svg" width="50"> | <img src="https://upload.wikimedia.org/wikipedia/commons/7/75/Django_logo.svg" width="50"> | <img src="https://www.django-rest-framework.org/img/logo.png" width="100"> | <img src="https://www.sqlite.org/images/sqlite370_banner.gif" width="100"> |



## Setup Locally
- **First clone repo locally**  
  **Run below command in terminal**  
  `git clone https://github.com/Mehmood007/drf_ecommerce`


- **Navigate to Directory**   
`cd drf_ecommerce`

- **Install Dependencies**  
  - First make sure virtual environment is activated  
  - Make sure you have postgres installed on system and running  
`pip install -r requirements.txt`

- **Setup .env**  
  - Create `.env` file inside project  
  - Look into `.env-sample` and fill `.env` accordingly  


- **Run Migrations in app directory**    
  `python manage.py migrate`


- **Run Server**  
  - First make sure everythin is fine and run test cases.  
  - To run test case just type `pytest` and press enter  
  - If everything is fine then start server  
  `python manage.py runserver`