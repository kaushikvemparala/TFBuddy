# TFBuddy
Upload TFEvent file and plot info you want from it.

## Setup
Run the following commands
```
$ git clone https://github.com/kaushikvemparala/TFBuddy.git
$ cd TFBuddy
$ pip install virtualenv # if you dont have vitualenv installed
$ python -m venv TFBuddy
$ source TFBuddy/bin/activate
$ pip install -r requirements.txt
```

## How to run
Run the following commands from the TFBuddy directory:
```
$ python back/server.py
```

Then, open a new terminal session and run the following commands from the `TFBuddy` directory:
```
$ source TFBuddy/bin/activate
$ cd src
$ npm start
```
