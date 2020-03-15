# meep-backend

## Setup

## Docker-compose

1. Install Docker. Compose should be bundled with it.
2. Start the containers: `docker-compose up --build -d`.
3. Seed the development database: `docker container exec meep-backend_api_1 python /meep/api/src/db_operations.py reset dev`. You should only need to do this the first time you run the app.
4. In a browser, or some other client, type `localhost/api/locations`. If you see a bunch of json data, it worked!

### Useful docker commands

- Shell into database:

  ```sh
  docker container exec -it meep-backend_db_1 psql -U meep -h meep-backend_db_1 -d meep_api
  ```

  password: `supersafe`

- Shell into api container

  ```sh
  docker container exec -it meep-backend_api_1 /bin/ash
  ```

- Shell into nginx container

  ```sh
  docker container exec -it meep-backend_web_server_1 /bin/bash
  ```

- view log files (similar for api)

  ```sh
  docker logs meep-backend_web_server_1
  ```

### Run only the api container with Docker

1. Install Docker
2. Build docker image from dockerfile:

   ```sh
   docker build -t meep-backend:gunicorn src
   ```

3. Create and run a container from the image:

   ```sh
   docker run -p 8001:8000 meep-backend:gunicorn
   ```

   or to allow live editing of the code in the container, do

   ```sh
   docker run -p 8001:8000 -v $(pwd)/src:/meep/api/src meep-backend:gunicorn
   ```

   - On windows, the command for live editing probably won't work. instead of `$(pwd)/src` on the left side of the bind mount, you will have to provide an absolute path to the project folder that contains the Dockerfile (src at the time of writing). After that, there is a chance that you will get a different error. Restart docker and try again. It usually works on the second attempt. Please note that this is a temporary workaround while we find a less annoying way to run the project on windows.

4. In a browser, try typing `http://localhost:8001/locations` to see
   if it worked.

### Unix without docker

1. Install python

   ```sh
   sudo apt-get install python3
   ```

2. [Install virtualenv](https://virtualenv.pypa.io/en/latest/installation/)

   ```sh
   sudo apt install virtualenv
   ```

3. Clone the master branch

   ```sh
   git clone git@github.com:codeforkansascity/meep-backend.git
   ```

4. Move into project root directory

   ```sh
   cd meep-backend
   ```

5. Create a virtual environment in the project root directory

   ```sh
   virtualenv venv
   ```

6. Activate the virtual environment

   ```sh
   source venv/bin/activate
   ```

7. Install python requirements

   ```sh
   pip install -r src/requirements.txt
   ```

8. Install sqlite3

   ```sh
   sudo apt install sqlite3
   ```

9. Create a sqlite database

   ```sh
   touch dev.db
   ```

10. Set dev database environment variable

    ```sh
    export DEV_DATABASE_URL=sqlite:///dev.db
    ```

11. Open the database in sqlite

    ```sql
    sqlite3 dev.db;
    ```

    Check to see if it created the tables with `.tables`

12. Try to display data from a table. You should see a list of projects display.

    ```sql
    select * from projects;
    ```

13. Set flask environment variable to development

    ```sh
    export FLASK_ENV=development
    ```

14. Set flask app environment variable

    ```sh
    export FLASK_APP="src/app:create_app()"
    ```

15. Run the app

    ```sh
    flask run
    ```

16. Test to see if it worked: in a browser, type `localhost:5000/projects` you should see some json containing project data

### Windows without docker

1. Install python
2. Install pip
3. Install virtualenv
4. Clone the master branch
5. Create a virtual environment in the project root directory
6. Activate the virtual environment `venv\\Scripts\\activate`
7. Pip install requirements `pip install -r requirements.txt`
8. Set dev database environment variable `set DEV_DATABASE_URL=sqlite:///dev.db`
9. Set flask environment variable to development

   ```sh
   set FLASK_ENV=development
   ```

10. Set flask app variable to point towards app.py

    ```sh
    set FLASK_APP=src\app.py
    ```

11. Run the app

    ```sh
    flask run
    ```

12. Test to see if it worked: in a browser, type `localhost:5000/projects` you should see some json containing project data

### Tests

1. Start the containers as normal: `docker-compose up --build -d`
2. Run pytest in the api container to run all discovered tests: `docker exec -it meep-backend_api_1 pytest`
   - Optionally, shell into the api container as normal (`docker container exec -it meep-backend_api_1 /bin/ash`) and then enter the `pytest` command

- Add -v command line argument for more detailed view of both failing **_and_** passing tests: `pytest -v`
- Only run tests in a specific package by specifying its directory: `pytest ../tests/unit`
- Only run tests in a specific module by specifying its directory and filename: `pytest ../tests/unit/test_models.py`
- Only run a specific test in a specific module: `pytest ../tests/unit/test_models.py::test_insert_location`

### meep Shell Script

- Checkout the `meep` shell script in the root directory for some shorter ways of running some of these commands with either the shell script itself or by copying the shorthand aliases into your dev environment.
