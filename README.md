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

## Launch Instructions:
Click this link to go to our website: [Live Link](http://167.99.145.123/)
### To Install and run on localhost:
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

### To Install and run on Apache2:
1. SSH into your droplet by entering ```ssh <user>@<your ip address>``` into your terminal.
2. Grant yourself sudo acess by entering '''sudo su''' into your terminal. 
3. Move to the directory where the project will be located by entering ```cd /var/www/```. Then create a directory for the project by typing ```mkdir borkbook``` and after ```cd borkbook```.
4. Clone the repo ```$ git clone https://github.com/th0mazzz/onUltimateTrack.git```.
5. Replace the ```<ip address>``` after ServerName with your own ip address in borkbook.conf. 
6. Change the permissions by entering ```chgrp -R www-data ccereal``` and ```chmod -R g+w ccereal```.
7. Install all the dependencies needed by typing ```$pip install -r <path-to-file>requirements.txt```.
8. Move the .conf file to the site-enabled directory by typing ```$ mv borkbook/borkbook.conf ~/etc/apache2/sites-enabled/```.
9. Enable the site by entering ```a2ensite borkbook``` in the terminal. 
10. Either reload or restart the apache2 server by typing ```service apache2 reload``` or ```service apache2 restart```. 
11. Enter your ip address into your browser and enjoy our web application!

## Dependencies:
* Flask==1.0.2  
   Used as the framework for the app.
* Jinja2==2.10  
   Template engine for Python.  

1. Install the dependencies listed above by typing ```(venv)$pip install -r <path-to-file>requirements.txt``` in your terminal.
