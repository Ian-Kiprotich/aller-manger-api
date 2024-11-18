# REST APIs with Python FastAPI - Aller Manger API
## Aller Manger Restaurant API Demo
Featuring FastAPI + MongoDB + (HTML,CSS,JS)

by <a href="https://github.com/tiprock-network"><b>Theophilus Owiti</b></a>

### Introduction
This REST API will give you a quick introduction in bulding REST APIs with Python, especially using FastAPI. FastAPI has powerful features that allow you to get up and running really quickly .e.g. automated documentation(automatic Swagger UI Set Up, Redocs Set Up), it's asynchronous nature that takes up the cooroutines approach, support for easy routing making it easy for someone coming from a framework like Express.js to understand quickly, and many more features.

In this tutorial we shall be setting up fastapi and creating endpoints that would be later on be protected using JWT tokens. If you like this work, don't be shy to give it a star :)

<img src="aller_manger_frontend/assets/allerManger.gif" style="height:400px; width:100%; object-fit:contain;" alt="picture of aller manger app" />


### Setting Up
Before we get started you need to have :
* MongoDB Compass Community Edition Installed (or you can use your MongoDB account database connection string Atlas URL)
* VS Code installed
* You may require Azure credits if you are planning to test deployment
* Python 3.10 +  installed
* Create a Postman Account
* Install the python extension in VS Code
* Install the Postman extension in VS Code

### Prepare your work environment

* Load the project locally from your account to the machine, fork the repository to your account and git clone it to your local PC. After forking here are the steps you'd wanna follow:

    Get the fork git url link and do a git clone, replace example url below with the actual URL 
    ```
    cd desktop
    ```

    ```
    git clone https//... .git
    ```

    ```
    cd aller-manger-api
    ```

* Now that you are in aller-manger-api folder, go ahead and set up the things you need, like this

    Create a new python environment
    ```
    cd app
    ```

    ```
    python -m venv .venv
    ```

    Install the required python packages after activating the virtual environment
    For windows only (Powershell)
    ```
    .venv\Scripts\Activate.ps1
    ```

    Windows: ``` python -m venv .venv``` Activate using powershell: ``` .venv\Scripts\Activate.ps1 ```

    Linux/MacOS: ``` python3 -m venv .venv ``` then ``` source venv/bin/activate ```

    Installing packages
    ```
    pip install -r requirements.txt
    ```

* Fireup FastAPI and start following the tutorial or make changes
    ```
    fastapi dev main.
    ```

## Using the REST API
 You might want to start using the base URL : http://127.0.0.1:8000/api/aller-manger/v1.0/" with postman.

 Now use main.py as your guide and complete the challenges and exercises.

## Front End
Simple just Open the index.html from aller_manger_frontend folder

