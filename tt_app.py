from flask import Flask, request
import jinja2
import re

import time
import datetime

import tclock

file_loader = jinja2.FileSystemLoader("templates")
env = jinja2.Environment(loader=file_loader)
template = env.get_template('html_example.jinja2')


app = Flask(__name__)

@app.route('/')
def index():
    now = datetime.datetime.now().strftime("%H:%M:%S")
    page = display_time(now)

    return page

@app.route('/show/<time>', methods=['GET'])
def show_time(time):
    time = process_time_string(time)
    page = display_time(time)
    return page

def process_time_string(tstring):
    matches = re.findall(":", tstring)
    if len(matches)==2:
        return tstring
    if len(matches)==1:
        return tstring + ":00"
    if len(matches)==0:
        return tstring + ":00:00"

def display_time(strtime):
    # Add error code dealing with bad strtime formatting
    try:
        valid_str_time = time.strptime(strtime, "%H:%M:%S")
    except ValueError: # bad time, so use now
        strtime = datetime.datetime.now().strftime("%H:%M:%S")
    return template.render(language_code="en", title="Time Teller", appname="timeteller", content=tclock.clock_face(strtime))

if __name__ == '__main__':

    app.run(debug=True)
