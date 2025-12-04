# Inventory Management System

REST API for stock management of a retail store chain

## Endpoints
#### Product Management
- GET /api/products
    - List of Products
    - Filters: Category, Price (Min, Max), Stock(Boolean)
    - Pagination
- GET /api/products/{id}
    - Product Detail
- POST /api/products
    - Create new Product
    - Mandatory fields: Name, Description, Category, Price, SKU
- PUT /api/products/{id}
    - Update existing Product
- DELETE /api/products/{id}
    - Delete Product
#### Stock Management
- GET /api/stores/{id}/inventory
    - List of Stores
    - Pagination
- GET /api/stores/{id}/inventory
    - List of Inventory by Store
- POST /api/inventory/transfer
    - Transfer Inventory between Stores
    - Validates againt Inventory Quantities
- GET /api/inventory/alerts
    - List of products with quantity below minimum

## Architecture and Technical Decisions

This API has been built using Django Framework an PostgreSQL v17 database.

Although other frameworks and architectures were considered, such as FastApi, Flask and Serverless Framework for AWS; this API has been built using Django due to the following reasons:

- ORM 
    - Database is modeled using OOP classes
    - Migrations allow to have a programatic version control over database definition.
- DRF
    - Generic classes for API design
    - Model serializers
    - Pagination features
    - Highly customizable, performant filters
- Testing 
    - Django and DRF provides with out-of-the-box classes to make testing easier

## Local Development

### Prerrequisites

You will need to create a virtual environment. You can use `pyenv` and `pyenv virtualenv` extension. Please refer to this [article](https://realpython.com/intro-to-pyenv/) for more information. Then, install Pyenv and Python 3.12.

You also need to setup a Postgres database. Recommended version is Postgres 17. Please refer to `.env.example` file for the values you need to provide to the application. Make sure that provided user has full privileges over the database.

> Tip - You can also use the database created by docker-compose file, in the **Image Build** section below.

Finally, please fill up .env file to load ENV variables to your terminal session. You can use .env.example to look for the required values.

### Local Setup

At the repository root, please run below commands to create and activate Python virtual enviroment.

- `pyenv virtualenv 3.12.11 <enviroment_name>`
- `pyenv activate environment name`

Once the environment is activated, please install dependencies by running:
- `pip install -r backend/requirements.txt`

Please load the enviroment variables by running
-  `source .env`

Before running the server for the first time, and with your database reachable, please setup the database by running
- `python backend/manage.py migrate`

If you want to populate with mock data, please run the following. 
- `python backend/manage.py populate_catalogs 10 5`
- Numeric parameters are intended for the number of products and stores, respectively.
- This command will create Inventory for all products in all stores created at this execution. In above example, 10 Products, 5 Stores and 5*10 Inventory will be created.

Now you can start the server by running
- `python backend/manage.py runserver`

API endpoints will be under `http://localhost:8000/api/` URL. E.g. 
- `http://localhost:8000/api/products/`

Now you will be ready to contribute to this project.

> Note - Don't forget to append `/` at the end of each URL, right before query parameters

Additionally, you can find API documentation under:
- `http://localhost:8000/api/schema/`
    - API Schema
- `http://localhost:8000/api/docs/`
    - Swagger UI

Last but not least, you can run Unit and Integration tests using the following command:

- `python backend/manage.py test inventory`

#### Appendix: Admin Site
You can also manage Inventory through Admin Site UI. You will need to create a super user by running:
- `python backend/manage.py createsuperuser`

You will need to provide username, email and password. After this step, you can log in to Admin Site under:
- `http://localhost:8000/admin/`

### Image Build - Local

Please make sure you have Docker and docker compose installed.
Docker compose file has the following services: 
- Django Backend
- Postgres Database

You can build and start Application by running, at the root of the repository:

- `sudo docker compose up --build`

This command will download all Docker images, build the project, and start the containers. Once completed, you can access Django application at `http://localhost:8000`

You will need to setup the database by running:
-  `sudo docker compose run django-be python manage.py migrate`

You can now interact with the Django application by running commands such as the one above. For instance, to populate data, please run:

-  `sudo docker compose run django-be python manage.py migrate`

Please refer to **Local Setup** Section for more detailed interactions with Django backend.

## Deployment

Please refer to `Deployment.md` document

> Disclaimer - Document built using AI assistance.

## Architecture Diagram

Please refer to `architecture.png` file

