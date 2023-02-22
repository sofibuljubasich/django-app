# Task manager app
Task Manager is a Django Web Application that helps you maintain your tasks and To-DOs.It includes user registration and login, CRUD of tasks and mark your pending tasks as completed.
## Setup

1. Clone the repository:
```sh
$ git clone https://github.com/sofibuljubasich/django-app.git
$ cd django-app
```
2. To setup this project, create a virtual environment using Python 3.6 or higher and run the following command in your terminal (ensure that you are in the project directory):
    ```bash
    $ pip install -r requirements.txt
    ```

   <p>It will set your environment up to run the project</p>

3. Run the following commands in your terminal:
    ```bash
    python manage.py makemigrations
    python manage.py migrate
    python manage.py runserver
    ```  

    This will set your SQL database up and run your local server.
    Navigate to `http://127.0.0.1:8000`.
    Press ```ctrl+c``` to stop the server.

Do remember to run ```python manage.py makemigrations``` in your terminal before committing changes.

