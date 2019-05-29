# Borkbook :notebook_with_decorative_cover:  
## onUltimateTrack - Thomas Zhao, Xiaojie (Aaron) Li, Stefan Tan, Johnny Wong 
For the Ultimate Track team :sunglasses:

## Roles
### Thomas Zhao
* Project Manager
* Database Manager (SQLite)
### Xiaojie (Aaron) Li
* Frontend Developer (HTML, CSS)
* App Developer (app.py, Python)
### Stefan Tan
* SVG Manipulator (SVG, JavaScript)
* App Developer (app.py, Python) 
### Johnny Wong
* Database Manager (SQLite)
* SVG Manipulator (SVG, JavaScript)

## Overview:
TL;DR: Playbook for teams of any sport!  
Borkbook is a web-based application that aids teams by organizing their playbooks, rosters, and game stats. It would be helpful for teams to better communicate and explain plays through visuals (created using SVG and stored in a database) while making them easily accessible and editable by the creator and team admin.

## Instructions to Run:
Click this link to go to our website: [Live Link](http://167.99.145.123/)
### To Run Locally:
1. Open a terminal session.
2. Create your own environment by typing (name is a placeholder for the name of the virtual environment of your choosing):
```
$ python3 -m venv name
```
3. Activate the virtual environment by typing ```$ . name/bin/activate``` in the terminal and make sure it is running python3 by typing ```(venv)$ python --version``` in the terminal.
4. Clone this repository. If you have already cloned this repository, skip this step. To clone this repo, navigate to the directory you want for this repository to located in. Then clone using SSH by typing ```(venv)$ git clone git@github.com:th0mazzz/onUltimateTrack.git``` or clone using HTTPS by typing ```(venv)$ git clone https://github.com/th0mazzz/onUltimateTrack.git``` in the terminal.
5. Navigate to our project by typing ```$ cd onUltimateTrack/borkbook/``` in the terminal.
6. Make sure you have all the dependencies installed in your virtual environment. To check, look at the [Dependencies section](https://github.com/th0mazzz/onUltimateTrack#dependencies) below.
7. Run the python file by typing ```(venv)$ python __init__.py``` in the terminal.
8. This should appear in the terminal after running the python file.   
```
* Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
* Restarting with stat
* Debugger is active!
* Debugger PIN: 248-748-502
```

9. Open a web browser and navigate to the link http://127.0.0.1:5000/.
10. Register if you are a new user or login if you are an existing user and enjoy our web application! 

## Dependencies:
* Flask==1.0.2

   Used as the framework for the app.
* Jinja2==2.10

1. Install the dependencies listed above by typing ```(venv)$pip install -r <path-to-file>requirements.txt``` in your terminal.
