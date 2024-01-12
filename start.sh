#!/bin/sh

echo

cd /home/pi/dev/git/datacollector
. alviso/bin/activate
pip install -r requirements.txt
python app.py
