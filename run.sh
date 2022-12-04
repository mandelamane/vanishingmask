#/bin/bash

export FLASK_APP=apps.vanishingmask.app.py
( sleep 5; open http://127.0.0.1:5000/ ) & flask run
