# sensornetworks-dash

> Simple example of [Dash](https://plot.ly/dash) framework use to simiulate wireless sensor network key distribution algorithm

## Installation (Linux/MacOS)

```
$ git clone https://github.com/radekwlsk/sensornetworks-dash
$ cd sensornetworks-dash
$ python3 -m venv venv
$ source venv/bin/activate
(venv)$ pip install -r requirements
```

## Run dev server (Linux/MacOS)

```
$ source venv/bin/activate
(venv)$ python wsgi.py
```
That should result in local dev server start:
```
 * Serving Flask app "sensornetworks-dash" (lazy loading)
 * Environment: production
   WARNING: This is a development server. Do not use it in a production deployment.
   Use a production WSGI server instead.
 * Debug mode: off
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
```

Now just go to [http://127.0.0.1:5000/](http://127.0.0.1:5000/).
