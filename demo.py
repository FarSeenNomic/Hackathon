from flask import Flask
from flask import render_template, send_from_directory, request
import random

def similar(a, b):
    from difflib import SequenceMatcher
    return SequenceMatcher(None, a.lower(), b.lower()).ratio()

app = Flask(__name__)

@app.route('/')
def page1():
    return send_from_directory('static', "index.html")

schools = ["UCLA", "USC", "CPP"]

gen_eds = [
#    ["English",4],
#    ["Japanese",4],
#    ["Japanese II",4],
#    ["Dance",4],
#    ["Depression",4],
]

f = open("./Kassandra Code 2.csv", "r")
for line in f.read().split("\n"):
    ls = line.split(",")
    if len(ls) == 3:
        try:
            gen_eds.append([ls[1], int(ls[2])])
        except ValueError:
            pass
            print(f"VE at {ls}")

maj_eds = [
    ["Math 10",4],
    ["CALC I",4],
    ["CALC II",4],
    ["CALC III",4],
]

def get_random_classes_order():
    cl = random.sample(gen_eds, k=len(gen_eds))
    try:
        p1 = [name for name, a, b in cl].index("ENGL A100")
        if p1 != 0:
            cl[0],cl[p1] = cl[p1],cl[0]
    except ValueError:
        print("ENGL A100 failed")
    return cl

def handle_classes():
    global gen_eds
    global maj_eds
    edct = len(maj_eds)
    gened_index = 0

    classes_list = []
    sems = 4
    for i in range(sems):
        classes_list.append(maj_eds[int(i*edct/sems):int((i+1)*edct/sems)])

    GE_local = get_random_classes_order()
    for i in range(len(classes_list)):
        while sum(x[1] for x in classes_list[i]) < 12:
            classes_list[i].append(GE_local.pop())

            # Just for test cases
            # Please remember to remove
            if not GE_local:
                GE_local.append(["Depression",1])

    classes_output = []
    for index, sem_classes in enumerate(classes_list):
        classes_output.append(f"Semester {index} ({sum(units for c,units in sem_classes)} Units):")
        for c,units in sem_classes:
            classes_output.append(f"{c} for {units} Units")
    return classes_output

@app.route('/school')
def hello():
    schools_from = request.args.get('data').split(",")
    school_from = ",".join(schools_from)
    return render_template('school.html', school_from=school_from, classes=handle_classes())
    
    #if school_from in schools:
    #else:
    #    nearest = max(schools, key=lambda r: similar( r.upper(), school_from.upper() ))
    #    return render_template('school_error.html', school_from=school_from, DYM=nearest)

import os
@app.route('/garf')
def garf():
    files = os.listdir("D:/Pictures/garfield/")
    return send_from_directory("D:/Pictures/garfield/", random.choice(files))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=25565)
