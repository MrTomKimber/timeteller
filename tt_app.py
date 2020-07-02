from flask import Flask, request
import jinja2
import re

import time
import datetime

import tclock

file_loader = jinja2.FileSystemLoader("templates/")
static_folder = jinja2.FileSystemLoader("static/")
env = jinja2.Environment(loader=file_loader)
template = env.get_template('html_example.jinja2')


app = Flask(__name__)

@app.route('/')
def index():
    debug = False
    if "debug" in request.args:
        debug = bool_arg(request.args.get("debug"))
    now = datetime.datetime.now().strftime("%H:%M:%S")
    page = display_time(now, debug)
    return page

@app.route('/show/<time>/', methods=['GET'])
def show_time(time):
    debug = False
    if "debug" in request.args:
        debug = bool_arg(request.args.get("debug"))
    time = process_time_string(time)
    page = display_time(time,debug)
    return page

def bool_arg(b_string):
    if b_string.lower() in ["true", "yes", "y", "1"]:
        return True
    else:
        return False

def render_request():
    output_str="<div>"
    print(request.__dict__)
    for k,v in request.__dict__.items():
        print ( k,v)
        if isinstance(v,dict):
            output_str= output_str + "<p>{k} : </p>".format(k=k)
            for kk,vv in v.items():
                output_str = output_str + "<p style=\"text-indent: 40px\">{k} : {v}</p>".format(k=kk, v=str(vv))
        else:
            output_str= output_str + "<p>{k} : {v}</p>".format(k=k, v=str(v))
    return output_str+"</div>"

def process_time_string(tstring):
    matches = re.findall(":", tstring)
    if len(matches)==2:
        return tstring
    if len(matches)==1:
        return tstring + ":00"
    if len(matches)==0:
        return tstring + ":00:00"

def wrap_m_div(text):
    return "<div class=\"mid\">" + text + "</div>"




def display_time(strtime, debug=False):
    # Add error code dealing with bad strtime formatting

    try:
        valid_str_time = time.strptime(strtime, "%H:%M:%S")
    except ValueError: # bad time, so use now
        strtime = datetime.datetime.now().strftime("%H:%M:%S")
        print (render_request())
    strtime = process_time_string(strtime)
    analog_clock = tclock.clock_face(strtime)
    digital_clock = tclock.seven_seg_clock(strtime)
    time_text_simple = tclock.time_paragraph(strtime)
    content = wrap_m_div(analog_clock) + wrap_m_div(time_text_simple) + wrap_m_div(digital_clock)
    if debug:
        debug_content = str(type(debug)) + str(debug) + render_request()
    else:
        debug_content = ""
    return template.render(language_code="en", title="Time Teller", appname="timeteller", content= content + debug_content)

if __name__ == '__main__':

    app.run(debug=True)
