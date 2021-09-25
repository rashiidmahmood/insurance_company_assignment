# Insurance Company Assignment

## Docker setup
### Clone your repo
    $ git clone https://github.com/rashiidmahmood/insurance_company_assignment.git

### Make sure docker is installed on your system and run following commands inside your project directory:

    $ docker-compose build
    $ docker-compose up

### Interact with APIs on this URL:
    $ http://127.0.0.1:8000/api/schema/swagger/

### Authenticate for Car Create API using below credentials:
    username: admin@gmail.com
    password: admin@123$


## Development Steps

1. Install <b>git</b> on the system.
2. Open shell/command prompt and run following command to clone the project:
    <br>`$ git clone https://github.com/rashiidmahmood/insurance_company_assignment.git`


3. Make sure <b>python3</b> and <b>pip3</b> are installed on the system.
4. Once inside the project's root directory, install requirements using the following command:
    <br>Note: It's recommended to create a virtual environment and install requirements there.
    <br>`$ pip install -r ./requirements/local.txt`

5. Run this command inside the project directory to start the server:
    <br>`$ python3 manage.py runserver 8000`

6. Following URL will open swagger UI from where all the project APIs can be accessed:<br>
    http://127.0.0.1:8000/api/schema/swagger/

7. **Customer Create API** is the only public API to allow customers to register on our platform.
   This API is public and can be accessed without authentication except Car Create API.
   <br> All customers are created with this password:
    <br>`password: customer@123$` 

8. Customers can create new quotes after authenticating using their email/password. A customer can't create
   quote for other customer.
9. Staff user can also create quotes on customer's behalf.
10. Following credentials can be used to authenticate staff user:
    <br>`username: admin@gmail.com`
    <br>`password: admin@123$`
    Or new superuser can be created using below management command:
    <br>`$ python3 manage.py createsuperuser`


## Tests
Following command can be used to run test cases:


    $ python manage.py test


