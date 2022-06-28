from math import cos, sin, sqrt, pi
import time

import numberstrings as ns

def svg_radial_line_data(cx, cy, r, l, alpha):
    pointa = (cx + cos(alpha)*r, cy+sin(alpha)*r)
    pointb = (cx + cos(alpha)*(r+l), cy+sin(alpha)*(r+l))
    path_s = """d="M{x1} {y1}
                   L {x2} {y2}" """.format(x1=pointa[0],y1=pointa[1], x2=pointb[0],y2=pointb[1])
    return path_s


def svg_arc_segment_path_data(cx, cy, r, w, alpha, theta):
    # cx, cy describe the origin of the circle.
    # r      describes the radius
    # w      describes the width
    # alpha  describes the (clockwise) starting angle
    # theta  describes the angle scribed by the arc
    #print( alpha, theta)
    whole=False
    if theta == 2*pi:
        # Special case where the entire extent is taken up
        whole = True
        theta = theta * 0.5
    pointa = (cx + cos(alpha)*r, cy+sin(alpha)*r)
    pointb = (cx + cos(alpha+theta)*r, cy+sin(alpha+theta)*r)
    pointc = (cx + cos(alpha+theta)*(r+w), cy+sin(alpha+theta)*(r+w))
    pointd = (cx + cos(alpha)*(r+w), cy+sin(alpha)*(r+w))
    arc_points = [pointa, pointb, pointc, pointd]
    if theta > pi: # Where the arc-segment is greater than 180 degrees, use the long arc-flag
        asf=0
        nasf=1
        laf=1
        nlaf=1
    else:
        asf=0
        nasf=1
        laf=0
        nlaf=0
    if not whole:
        path_s = """d="M{x1} {y1}
                       A {r1} {r1} {xarot} {nlaf} {nasf} {x2} {y2}
                       L {x3} {y3}
                       A {r2} {r2} {xarot} {laf} {asf} {x4} {y4}
                       L {x1} {y1}
                       Z" """.format( x1=arc_points[0][0],
                     y1=arc_points[0][1],
                     r1=r,
                     r2=r+w,
                     xarot=0,
                     laf=laf,
                     nlaf=nlaf,
                     nasf=nasf,
                     asf=asf,
                     x2=arc_points[1][0],
                     y2=arc_points[1][1],
                     x3=arc_points[2][0],
                     y3=arc_points[2][1],
                     x4=arc_points[3][0],
                     y4=arc_points[3][1]
                    )
    else:
        path_s = """d="M{x1} {y1}
                    A {r1} {r1} 0 1 0 {x2} {y2}
                    A {r1} {r1} 0 1 0 {x1} {y1} Z
                    M {x3} {y3}
                    A {r2} {r2} 0 0 1 {x4} {y4}
                    A {r2} {r2} 0 0 1 {x3} {y3} Z"
                """.format( x1=arc_points[0][0],
                     y1=arc_points[0][1],
                     r1=r,
                     r2=r+w,
                     xarot=0,
                     laf=laf,
                     nlaf=nlaf,
                     nasf=nasf,
                     asf=asf,
                     x2=arc_points[1][0],
                     y2=arc_points[1][1],
                     x3=arc_points[2][0],
                     y3=arc_points[2][1],
                     x4=arc_points[3][0],
                     y4=arc_points[3][1]
                    )
    return path_s

def svg_arc_segment_text_path_data(cx, cy, r, w, alpha, theta):
    #TODO - fill this with a path, along which text can be strung
    whole=False
    if theta == 2*pi:
        # Special case where the entire extent is taken up
        whole = True
        theta = theta * 0.5

    pointa = (cx + cos(alpha)*(r+(w/3)), cy+sin(alpha)*(r+(w/3)))
    pointb = (cx + cos(alpha+theta)*(r+(w/3)), cy+sin(alpha+theta)*(r+(w/3)))
    if theta > pi: # Where the arc-segment is greater than 180 degrees, use the long arc-flag
        asf=0
        nasf=1
        laf=1
        nlaf=1
    else:
        asf=0
        nasf=1
        laf=0
        nlaf=0
    if not whole:
        path_s = """d="M{x1} {y1}
                       A {r1} {r1} {xarot} {nlaf} {nasf} {x2} {y2}" """.format( x1=pointa[0],
                     y1=pointa[1],
                     r1=r+(w/3),
                     xarot=0,
                     laf=laf,
                     nlaf=nlaf,
                     nasf=nasf,
                     asf=asf,
                     x2=pointb[0],
                     y2=pointb[1])
    else:
        path_s = """d="M{x2} {y2}
                    A {r1} {r1} 0 1 1 {x1} {y1}"
                """.format( x1=pointa[0],
                  y1=pointa[1],
                  r1=r+(w/3),
                 xarot=0,
                 laf=laf,
                 nlaf=nlaf,
                 nasf=nasf,
                 asf=asf,
                 x2=pointb[0],
                 y2=pointb[1])
    return path_s


def style_dict_to_attribute_string(style_dict):
    return " ".join(["{k}=\"{v}\"".format(k=str(k), v=str(v)) for k,v in style_dict.items()])

def svg_radial_line(rad_lin_d, s_class=None):
    base = """<path {d} {c}/>"""
    if s_class is not None:
        style_class = "class=\"{c}\"".format(c=s_class)
    else:
        style_class = ""
    return base.format(d=svg_radial_line_data(**rad_lin_d), c=style_class)



def svg_arc_segment(prefix, arc_seg_d, id=None,title=None, s_class=None, t_class=None, tp_class=None, tl_pc=None):
    # id=title, not a great idea - probably worth changing sooner than later.
    id=str(prefix) + str(id)
    if tl_pc is None:
        tl_pc = 3
    tl_pc_t = "{tl}%".format(tl=str(tl_pc))
    if title is not None:
        text_path_id = "text_path__" + id
    else:
        text_path_id = None
    base = """<g id="{id}" {c}>
                <path  {d}> {title} </path>
                <defs><path id="tpid_{id}" {tpd}/></defs>
                <text {tc}  textLength="{tl_pc_t}" lengthAdjust="spacingAndGlyphs">
                <textPath {tpc} href="#tpid_{id}" startOffset="50%">{t}</textPath></text>
              </g>"""
    if title is not None:
        title_content="<title>{t}</title>".format(t=title)
    else:
        title_content=""
    if s_class is not None:
        style_class = "class=\"{c}\"".format(c=s_class)
    else:
        style_class = ""
    if t_class is not None:
        text_class = "class=\"{tc}\"".format(tc=t_class)
    else:
        text_class = ""
    if tp_class is not None:
        text_path_class = "class=\"{tcp}\"".format(tcp=tp_class)
    else:
        text_path_class = ""



#    return base.format(d=svg_arc_segment_path_data(**arc_seg_d), style=styling, title=title, id=id, c=style_class)
    return base.format(d=svg_arc_segment_path_data(**arc_seg_d), tpd=svg_arc_segment_text_path_data(**arc_seg_d), title=title_content, t=title, id=id, text_path_id=text_path_id, c=style_class, tc=text_class, tpc=text_path_class, tl_pc_t=tl_pc_t)




def eo(n):
    if int(n/2)==n/2:
        return True
    return False

def clock_minute_arcs():
    minute_arcs = []
    tau=2*pi

    for i in range(0,60):
        tick = i*(tau/60)
        if i < 30:
            if eo(i):
                arc=svg_arc_segment("min", arc_seg_d={"cx":10,"cy":10,"r":9,"w":1,"alpha":tick+(tau/120),"theta":tau/60}, id=str(i+1), title=str(i+1), s_class="green", t_class="text_minute", tp_class="text_path_minute", tl_pc=2)
            else:
                arc=svg_arc_segment("min", arc_seg_d={"cx":10,"cy":10,"r":9,"w":1,"alpha":tick+(tau/120),"theta":tau/60}, id=str(i+1), title=str(i+1), s_class="green2", t_class="text_minute", tl_pc=2)
            if i+1 in (60, 15, 30, 45):
                arc=svg_arc_segment("min", arc_seg_d={"cx":10,"cy":10,"r":9,"w":1.3,"alpha":tick+(tau/120),"theta":tau/60}, id=str(i+1),title=str(i+1), s_class="green3", t_class="text_minute", tp_class="text_path_minute", tl_pc=2)
            elif i+1 in (5,10,20,25,35,40,50,55):
                arc=svg_arc_segment("min", arc_seg_d={"cx":10,"cy":10,"r":9,"w":1.3,"alpha":tick+(tau/120),"theta":tau/60}, id=str(i+1),title=str(i+1), s_class="green3", t_class="text_minute", tp_class="text_path_minute", tl_pc=2)
        else:
            if eo(i):
                arc=svg_arc_segment("min", arc_seg_d={"cx":10,"cy":10,"r":9,"w":1,"alpha":tick+(tau/120),"theta":tau/60}, id=str(i+1),title=str((60-(i+1))), s_class="pink", t_class="text_minute", tp_class="text_path_minute", tl_pc=2)
            else:
                arc=svg_arc_segment("min", arc_seg_d={"cx":10,"cy":10,"r":9,"w":1,"alpha":tick+(tau/120),"theta":tau/60}, id=str(i+1),title=str((60-(i+1))), s_class="pink2", t_class="text_minute", tl_pc=2)
            if i+1 in (60, 15, 30, 45):
                arc=svg_arc_segment("min", arc_seg_d={"cx":10,"cy":10,"r":9,"w":1.3,"alpha":tick+(tau/120),"theta":tau/60}, id=str(i+1),title=str((60-(i+1))), s_class="pink3", t_class="text_minute", tp_class="text_path_minute", tl_pc=2)
            elif i+1 in (5,10,20,25,35,40,50,55):
                arc=svg_arc_segment("min", arc_seg_d={"cx":10,"cy":10,"r":9,"w":1.3,"alpha":tick+(tau/120),"theta":tau/60},id=str(i+1), title=str((60-(i+1))), s_class="pink3", t_class="text_minute", tp_class="text_path_minute", tl_pc=2)


        minute_arcs.append(arc)

    return "\n".join(minute_arcs)


def clock_minute_ticks():
    tau=2*pi
    radial_minute_ticks=[]
    for i in range(0,60):
        tick = i*(tau/60)
        if i in (0, 5,10,15,20,25,30,35,40,45,50,55):
            radial_minute_ticks.append(svg_radial_line(rad_lin_d={"cx":10,"cy":10,"r":8.5,"l":0.5,"alpha":tick},s_class="heavy black"))
        else:
            radial_minute_ticks.append(svg_radial_line(rad_lin_d={"cx":10,"cy":10,"r":8.5,"l":0.5,"alpha":tick},s_class="black"))

    return "\n".join(radial_minute_ticks)


def clock_hour_arcs():
    tau=2*pi
    hour_arcs=[]
    for i in range(0,12):
        tick = i*(tau/12)
        if eo(i):
            hour_arcs.append(svg_arc_segment("hour", arc_seg_d={"cx":10,"cy":10,"r":5,"w":3.5,"alpha":tick+(tau/24),"theta":tau/12}, id=str(i+1),title=str(i+1), s_class="blue1", t_class="text_hour",tl_pc=5))
        else:
            hour_arcs.append(svg_arc_segment("hour", arc_seg_d={"cx":10,"cy":10,"r":5,"w":3.5,"alpha":tick+(tau/24),"theta":tau/12}, id=str(i+1),title=str(i+1), s_class="blue2", t_class="text_hour", tp_class="text_path_hour",tl_pc=5))

    return "\n".join(hour_arcs)


def clock_hour_ticks():
    tau=2*pi
    radial_hour_ticks=[]
    for i in range(0,12):
        tick = i*(tau/12)
        radial_hour_ticks.append(svg_radial_line(rad_lin_d={"cx":10,"cy":10,"r":4.5,"l":0.5,"alpha":tick},s_class="black"))

    return "\n".join(radial_hour_ticks)



def hour_hand(htime):
    tau=360
    the_time = time.strptime(htime,"%H:%M:%S")
    degrees=((((the_time.tm_hour%12)+the_time.tm_min/60)/12)*tau)-90

    return f"""<path transform="rotate({degrees}, 10,10)" d="M 9.65 8
          L 9.65 14
          L 10 14.8
          L 10.35 14
          L 10.35 8 Z"
    class = "yellow alpha" />"""


def minute_hand(htime):
    tau=360
    the_time = time.strptime(htime,"%H:%M:%S")

    degrees=(((the_time.tm_min/60))*tau)-90

    return f"""<path transform="rotate({degrees}, 10,10)" d="M 9.65 8
          L 9.65 18
          L 10 18.8
          L 10.35 18
          L 10.35 8 Z"
    class = "yellow alpha" />"""

def clock_digits(htime):
    tds = ["sevenseg_{d}".format(d=htime[i]) for e,i in enumerate([0,1,3,4])]
    return tds



def twelve_hour(hour):
    if hour > 12:
        return hour - 12
    elif hour == 0 :
        return 12
    else:
        return hour

def twentyfour_hour(hour):
    return hour




def time_text(tstring, h24=False, style="simple"):
    stime = tstring
    try:
        stime = time.strptime(stime, "%H:%M:%S")
    except ValueError: # bad time, so use now
        stime = datetime.datetime.now().strftime("%H:%M:%S")
        print (render_request())

    hour = int(stime.tm_hour)
    if not h24:
        adj_h = twelve_hour
    else:
        adj_h = twentyfour_hour

    if style=="simple":

        minute = int(stime.tm_min)
        if minute!=0:
            if minute < 10:
                min_w = "oh-" + ns.number_to_text(minute)
            else:
                min_w = ns.number_to_text(minute)
            time_string = (ns.number_to_text(adj_h(hour)) + " " + min_w)

        else:
            cardinal = ns.clock_cardinals.get(minute)
            time_string= (ns.number_to_text(adj_h(hour)) + " " + cardinal)


    elif style=="proper":
        minute = int(stime.tm_min)
        if minute in [15,30,45]: # pick cardinal phrase
            cardinal = ns.clock_cardinals.get(int(stime.tm_min))
            if minute < 31:
                time_string= (cardinal + " " + ns.number_to_text(adj_h(hour)))
            else:
                time_string= (cardinal + " " + ns.number_to_text(adj_h(hour+1)))
        elif minute in [0]: # pick cardinal phrase
            cardinal = ns.clock_cardinals.get(minute)
            time_string= (ns.number_to_text(adj_h(hour)) + " " + cardinal)
        else:
            if minute == 1:
                time_string = ns.number_to_text(minute) + " minute past " + ns.number_to_text(adj_h(hour))
            elif 1 < minute < 30:
                time_string = ns.number_to_text(minute) + " minutes past " + ns.number_to_text(adj_h(hour))
            elif 30 < minute < 60:
                time_string = ns.number_to_text(60-minute) + " minutes to " + ns.number_to_text(adj_h(hour+1))
            else:
                time_string = ns.number_to_text(60-minute) + " minute to " + ns.number_to_text(adj_h(hour+1))
    return time_string

def time_paragraph(htime):

    return "<blockquote><i> {tt}</i> </blockquote>".format(tt=time_text(htime,style="proper"))


def seven_seg_clock(vtime):
    d1,d2,d3,d4=clock_digits(vtime)
    sevenseg = """
    <svg xmlns="http://www.w3.org/2000/svg" width="100%" viewbox="0 0 200 80" >
    <style>
        text {{font-size:0.04em;}}
        .white {{ fill: white; stroke: black; stroke-width:0.1;}}
        .darkgrey {{ fill: #222233; stroke: black; stroke-width:0.1;}}
        .yellow {{ fill: yellow; stroke: black; stroke-width:0.1;}}
        .orange {{ fill: #ffc78f; stroke: black; stroke-width:0.1;}}
        .pink {{ fill: #ffccff; stroke: black; stroke-width:0.1;}}
        .pink2 {{ fill: #ffe0ff; stroke: black; stroke-width:0.1;}}
        .pink3 {{ fill: #ff8888; stroke: black; stroke-width:0.1;}}
        .red {{ fill: #ff4444; stroke: black; stroke-width:0.1;}}
        .black {{ fill: black; stroke: black; stroke-width:0.1;}}
        .gray {{ fill: gray; stroke: silver; stroke-width:0.1;}}
        .green {{ fill: #c2ff85; stroke: black; stroke-width:0.1;}}
        .green2 {{ fill: #e4ffc8; stroke: black; stroke-width:0.1;}}
        .green3 {{ fill: #88ff33; stroke: black; stroke-width:0.1;}}
        .lime {{ fill: #ccff41; stroke: black; stroke-width:0.1;}}
        .blue1 {{ fill: #33ccff; stroke: black; stroke-width:0.1;}}
        .blue2 {{ fill: #7adeff; stroke: black; stroke-width:0.1;}}
        .heavy {{ fill: black; stroke: black; stroke-width:0.2;}}
        .alpha {{ fill-opacity:0.95;}}
    </style>

    <defs>
    <g id="sevenseg_1" class="lime" ><path d="M 1 1 L 2 2 L 11 2 L 12 1 L 11 0 L 2  0 Z" class="darkgrey"> </path>
                <path d="M 1 1 L 0 2 L 0 11 L 1 12 L 2 11 L 2  2 Z" class="darkgrey"> </path>
                <path d="M 12 1 L 11 2 L 11 11 L 12 12 L 13 11 L 13  2 Z" > </path>
                <path d="M 1 12 L 2 13 L 11 13 L 12 12 L 11 11 L 2  11 Z" class="darkgrey" > </path>
                <path d="M 1 12 L 0 13 L 0 22 L 1 23 L 2 22 L 2 13 Z" class="darkgrey" > </path>
                <path d="M 12 12 L 11 13 L 11 22 L 12 23 L 13 22 L 13 13 Z" > </path>
                <path d="M 1 23 L 2 24 L 11 24 L 12 23 L 11 22 L 2 22 Z" class="darkgrey" > </path>
    </g>

    <g id="sevenseg_2" class="lime"><path d="M 1 1 L 2 2 L 11 2 L 12 1 L 11 0 L 2  0 Z" > </path>
                <path d="M 1 1 L 0 2 L 0 11 L 1 12 L 2 11 L 2  2 Z" class="darkgrey"> </path>
                <path d="M 12 1 L 11 2 L 11 11 L 12 12 L 13 11 L 13  2 Z" > </path>
                <path d="M 1 12 L 2 13 L 11 13 L 12 12 L 11 11 L 2  11 Z"  > </path>
                <path d="M 1 12 L 0 13 L 0 22 L 1 23 L 2 22 L 2 13 Z" > </path>
                <path d="M 12 12 L 11 13 L 11 22 L 12 23 L 13 22 L 13 13 Z" class="darkgrey"> </path>
                <path d="M 1 23 L 2 24 L 11 24 L 12 23 L 11 22 L 2 22 Z" > </path>
    </g>

    <g id="sevenseg_3" class="lime" ><path d="M 1 1 L 2 2 L 11 2 L 12 1 L 11 0 L 2  0 Z" > </path>
                <path d="M 1 1 L 0 2 L 0 11 L 1 12 L 2 11 L 2  2 Z" class="darkgrey"> </path>
                <path d="M 12 1 L 11 2 L 11 11 L 12 12 L 13 11 L 13  2 Z" > </path>
                <path d="M 1 12 L 2 13 L 11 13 L 12 12 L 11 11 L 2  11 Z"  > </path>
                <path d="M 1 12 L 0 13 L 0 22 L 1 23 L 2 22 L 2 13 Z" class="darkgrey" > </path>
                <path d="M 12 12 L 11 13 L 11 22 L 12 23 L 13 22 L 13 13 Z" > </path>
                <path d="M 1 23 L 2 24 L 11 24 L 12 23 L 11 22 L 2 22 Z"  > </path>
    </g>

    <g id="sevenseg_4" class="lime"><path d="M 1 1 L 2 2 L 11 2 L 12 1 L 11 0 L 2  0 Z" class="darkgrey"> </path>
                <path d="M 1 1 L 0 2 L 0 11 L 1 12 L 2 11 L 2  2 Z" class="lime"> </path>
                <path d="M 12 1 L 11 2 L 11 11 L 12 12 L 13 11 L 13  2 Z" class="lime"> </path>
                <path d="M 1 12 L 2 13 L 11 13 L 12 12 L 11 11 L 2  11 Z"  class="lime"> </path>
                <path d="M 1 12 L 0 13 L 0 22 L 1 23 L 2 22 L 2 13 Z" class="darkgrey" > </path>
                <path d="M 12 12 L 11 13 L 11 22 L 12 23 L 13 22 L 13 13 Z" class="lime"> </path>
                <path d="M 1 23 L 2 24 L 11 24 L 12 23 L 11 22 L 2 22 Z"  class="darkgrey"> </path>
    </g>

    <g id="sevenseg_5" class="lime" ><path d="M 1 1 L 2 2 L 11 2 L 12 1 L 11 0 L 2  0 Z" > </path>
                <path d="M 1 1 L 0 2 L 0 11 L 1 12 L 2 11 L 2  2 Z" > </path>
                <path d="M 12 1 L 11 2 L 11 11 L 12 12 L 13 11 L 13  2 Z" class="darkgrey"> </path>
                <path d="M 1 12 L 2 13 L 11 13 L 12 12 L 11 11 L 2  11 Z"  > </path>
                <path d="M 1 12 L 0 13 L 0 22 L 1 23 L 2 22 L 2 13 Z" class="darkgrey" > </path>
                <path d="M 12 12 L 11 13 L 11 22 L 12 23 L 13 22 L 13 13 Z"> </path>
                <path d="M 1 23 L 2 24 L 11 24 L 12 23 L 11 22 L 2 22 Z"  > </path>
    </g>

    <g id="sevenseg_6" class="lime"><path d="M 1 1 L 2 2 L 11 2 L 12 1 L 11 0 L 2  0 Z" > </path>
                <path d="M 1 1 L 0 2 L 0 11 L 1 12 L 2 11 L 2  2 Z" > </path>
                <path d="M 12 1 L 11 2 L 11 11 L 12 12 L 13 11 L 13  2 Z" class="darkgrey"> </path>
                <path d="M 1 12 L 2 13 L 11 13 L 12 12 L 11 11 L 2  11 Z"  > </path>
                <path d="M 1 12 L 0 13 L 0 22 L 1 23 L 2 22 L 2 13 Z"  > </path>
                <path d="M 12 12 L 11 13 L 11 22 L 12 23 L 13 22 L 13 13 Z" > </path>
                <path d="M 1 23 L 2 24 L 11 24 L 12 23 L 11 22 L 2 22 Z"  > </path>
    </g>

    <g id="sevenseg_7" class="lime"><path d="M 1 1 L 2 2 L 11 2 L 12 1 L 11 0 L 2  0 Z" > </path>
                <path d="M 1 1 L 0 2 L 0 11 L 1 12 L 2 11 L 2  2 Z" class="darkgrey"> </path>
                <path d="M 12 1 L 11 2 L 11 11 L 12 12 L 13 11 L 13  2 Z" > </path>
                <path d="M 1 12 L 2 13 L 11 13 L 12 12 L 11 11 L 2  11 Z"  class="darkgrey"> </path>
                <path d="M 1 12 L 0 13 L 0 22 L 1 23 L 2 22 L 2 13 Z" class="darkgrey" > </path>
                <path d="M 12 12 L 11 13 L 11 22 L 12 23 L 13 22 L 13 13 Z" > </path>
                <path d="M 1 23 L 2 24 L 11 24 L 12 23 L 11 22 L 2 22 Z"  class="darkgrey"> </path>
    </g>


    <g id="sevenseg_8" class="lime"><path d="M 1 1 L 2 2 L 11 2 L 12 1 L 11 0 L 2  0 Z" > </path>
                <path d="M 1 1 L 0 2 L 0 11 L 1 12 L 2 11 L 2  2 Z" > </path>
                <path d="M 12 1 L 11 2 L 11 11 L 12 12 L 13 11 L 13  2 Z" > </path>
                <path d="M 1 12 L 2 13 L 11 13 L 12 12 L 11 11 L 2  11 Z" > </path>
                <path d="M 1 12 L 0 13 L 0 22 L 1 23 L 2 22 L 2 13 Z"  > </path>
                <path d="M 12 12 L 11 13 L 11 22 L 12 23 L 13 22 L 13 13 Z" > </path>
                <path d="M 1 23 L 2 24 L 11 24 L 12 23 L 11 22 L 2 22 Z"  > </path>
    </g>


    <g id="sevenseg_9" class="lime"><path d="M 1 1 L 2 2 L 11 2 L 12 1 L 11 0 L 2  0 Z" > </path>
                <path d="M 1 1 L 0 2 L 0 11 L 1 12 L 2 11 L 2  2 Z" > </path>
                <path d="M 12 1 L 11 2 L 11 11 L 12 12 L 13 11 L 13  2 Z" > </path>
                <path d="M 1 12 L 2 13 L 11 13 L 12 12 L 11 11 L 2  11 Z" > </path>
                <path d="M 1 12 L 0 13 L 0 22 L 1 23 L 2 22 L 2 13 Z" class="darkgrey" > </path>
                <path d="M 12 12 L 11 13 L 11 22 L 12 23 L 13 22 L 13 13 Z" > </path>
                <path d="M 1 23 L 2 24 L 11 24 L 12 23 L 11 22 L 2 22 Z"  class="darkgrey"> </path>
    </g>

    <g id="sevenseg_0" class="lime"><path d="M 1 1 L 2 2 L 11 2 L 12 1 L 11 0 L 2  0 Z" > </path>
                <path d="M 1 1 L 0 2 L 0 11 L 1 12 L 2 11 L 2  2 Z" > </path>
                <path d="M 12 1 L 11 2 L 11 11 L 12 12 L 13 11 L 13  2 Z" > </path>
                <path d="M 1 12 L 2 13 L 11 13 L 12 12 L 11 11 L 2  11 Z"  class="darkgrey"> </path>
                <path d="M 1 12 L 0 13 L 0 22 L 1 23 L 2 22 L 2 13 Z"  > </path>
                <path d="M 12 12 L 11 13 L 11 22 L 12 23 L 13 22 L 13 13 Z" > </path>
                <path d="M 1 23 L 2 24 L 11 24 L 12 23 L 11 22 L 2 22 Z"  > </path>
    </g>

    <g id="sevenseg_point"> <circle cx="0" cy="23" r="1"  class="lime"> </circle></g>

    <g id="sevenseg_colon"> <circle cx="0" cy="8" r="1"  class="lime"> </circle>
                            <circle cx="0" cy="16" r="1"  class="lime"> </circle>

    </g>



    </defs>
    <g transform="scale(2.0)">
    <rect x="2" y = "2" width="90" height="36" rx="4" class="darkgrey"/>
    <rect x="4" y = "4" width="86" height="32" rx="2"/>
        <g transform="skewX(-10)">
            <use xlink:href="#{d1}"     x="20" y="7.5" />
            <use xlink:href="#{d2}"     x="35" y="7.5" />
            <use xlink:href="#sevenseg_colon" x="50" y="7.5" />
            <use xlink:href="#{d3}"     x="52" y="7.5" />
            <use xlink:href="#{d4}"     x="67" y="7.5" />
        </g>
    </g>
    </svg>
    """.format(d1=d1, d2=d2, d3=d3, d4=d4)
    return sevenseg

def clock_face(vtime):

    return """
<svg xmlns="http://www.w3.org/2000/svg" width="100%" viewbox="-2 -2 25 25" >
    <style>
        text {{font-size:0.04em;}}
        .white {{ fill: white; stroke: black; stroke-width:0.1;}}
        .gray {{ fill: gray; stroke: silver; stroke-width:0.1;}}
        .darkgrey {{ fill: #222233; stroke: black; stroke-width:0.1;}}
        .yellow {{ fill: yellow; stroke: black; stroke-width:0.1;}}
        .orange {{ fill: #ffc78f; stroke: black; stroke-width:0.1;}}
        .pink {{ fill: #ffccff; stroke: black; stroke-width:0.1;}}
        .pink2 {{ fill: #ffe0ff; stroke: black; stroke-width:0.1;}}
        .pink3 {{ fill: #ff8888; stroke: black; stroke-width:0.1;}}
        .red {{ fill: #ffc78f; stroke: black; stroke-width:0.1;}}
        .black {{ fill: black; stroke: black; stroke-width:0.1;}}
        .green {{ fill: #c2ff85; stroke: black; stroke-width:0.1;}}
        .green2 {{ fill: #e4ffc8; stroke: black; stroke-width:0.1;}}
        .green3 {{ fill: #88ff33; stroke: black; stroke-width:0.1;}}
        .lime {{ fill: #ccff41; stroke: black; stroke-width:0.1;}}
        .blue1 {{ fill: #33ccff; stroke: black; stroke-width:0.1;}}
        .blue2 {{ fill: #7adeff; stroke: black; stroke-width:0.1;}}
        .heavy {{ fill: black; stroke: black; stroke-width:0.2;}}
        .alpha {{ fill-opacity:0.95;}}


        .text_minute {{
                       stroke:#000000;
                       fill:#000000;
                       stroke-width:0.02;
                       text-anchor:middle;
                       letter-spacing:0.0;
                       lengthAdjust:spacingAndGlyphs;}}

        .text_hour {{font-size:0.12em;
                       stroke:#000000;
                       fill:#ffffff;
                       stroke-width:0.05;
                       text-anchor:middle;
                       letter-spacing:1.0;}}
        .text_path_minute {{ }}

        .text_path_hour {{ }}
    </style>

<g transform='rotate(-90,10,10)'>

    {hour_str_segs}
    {minute_arc_segs}
    {radial_minute_ticks}
    {radial_hour_ticks}


    {hour_hand}
    {minute_hand}


    <circle cx=10 cy=10 r=0.1 > </circle>

</g>


</svg>
""".format(minute_arc_segs=clock_minute_arcs(),
           radial_minute_ticks=clock_minute_ticks(),
           hour_str_segs=clock_hour_arcs(),
           radial_hour_ticks=clock_hour_ticks(),
           hour_hand=hour_hand(vtime),
           minute_hand=minute_hand(vtime))
