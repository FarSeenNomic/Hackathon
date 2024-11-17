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

@app.route('/style.css')
def css():
    return send_from_directory('static', "style.css")

schools = ["UCLA", "USC", "CPP"]
gen_eds = []
maj_eds = []

#gen_eds is [short name, full name, requirements, units]

for file in [
    #"./Kassandra Code 2.csv",
    "./Area 1",
    "./Area 2 IGETC",
    "./Area 3",
    "./Area 5A IGETC",
    "./Area 6 IGETC",
    "./Area 7 IGETC"]:
    f = open(file, "r")
    for line in f.read().split("\n"):
        ls = line.split(",")
        if len(ls) == 3:
            try:
                gen_eds.append([ls[0], ls[1], "0", int(ls[2])])
            except ValueError:
                pass
                print(f"VE1 at {ls}")
        elif len(ls) == 4:
            try:
                gen_eds.append([ls[0], ls[1], ls[2], int(ls[3])])
            except ValueError:
                pass
                print(f"VE2 at {ls}")
        elif len(ls) == 1:
            pass
        else:
            print(ls)

maj_eds = {}
for file, school in [
    ["./majoring_classes.csv", "UCLA"],
    ["./CPP_maj.csv", "CPP"],
]:
    maj_eds[school] = []
    f = open(file, "r")
    for line in f.read().split("\n"):
        ls = line.split(",")
        if len(ls) == 4:
            try:
                maj_eds[school].append([ls[0], ls[1], ls[2], int(ls[3])])
            except ValueError:
                pass
                print(f"VE2 at {ls}")
        elif len(ls) == 1:
            pass
        else:
            print(ls)

def get_ges_classes_order():
    """
    puts the classes in a heap
    depending on their requirements
    """
    global gen_eds
    cl = random.sample(gen_eds, k=len(gen_eds))
    try:
        p1 = [short for short, full, reqs, units in cl].index("ENGL A100")
        if p1 != len(cl)-1:
            cl[~0],cl[p1] = cl[p1],cl[~0]
    except ValueError:
        print("ENGL A100 failed")

    for i in range(len(cl)):
        if cl[i][2] in "01":
            continue
        try:
            p1 = [short for short, full, reqs, units in cl].index(cl[i][2])
            if p1 < i:
                cl[i],cl[p1] = cl[p1],cl[i]
        except ValueError:
            print(f"{cl[i]} failed")

    return cl

#print("a")
#x=get_ges_classes_order()
#print("a")
#for i in x:
#    print(i)

def handle_classes(sems, school, inter, units, math):
    global gen_eds
    global maj_eds
    gened_index = 0
    try:
        local_maj_eds = maj_eds[school]
    except:
        print(f"invalid school {school}")
        local_maj_eds = maj_eds["UCLA"]
    if math:
        local_maj_eds = local_maj_eds[1:]
    edct = len(local_maj_eds)

    classes_list = []
    for i in range(sems):
        classes_list.append(local_maj_eds[int(i*edct/sems):int((i+1)*edct/sems)])

    GE_local = get_ges_classes_order()
    for i in range(len(classes_list)):
        print(1, classes_list[i])
        while sum(x[3] for x in classes_list[i]) < units:
            print(2, classes_list[i])
            classes_list[i].append(GE_local.pop())

            # Just for test cases
            # Please remember to remove
            if not GE_local:
                GE_local.append(["Depression",1])

    classes_output = []
    for index, sem_classes in enumerate(classes_list):
        classes_per_sem = []
        classes_per_sem.append(f"Semester {index+1} ({sum(units for short, full, reqs, units in sem_classes)} Units):")
        for short, full, reqs, units in sem_classes:
            classes_per_sem.append(f"{short}: {full} ({units} Units)")
        classes_output.append(classes_per_sem)

        if inter:
            classes_per_sem = []
            classes_per_sem.append(f"Interession:")
            short, full, reqs, units = GE_local.pop()
            classes_per_sem.append(f"{short}: {full} ({units} Units)")
            classes_output.append(classes_per_sem)

    return classes_output

@app.route('/school')
def hello():
    schools_from = request.args.get('data').split(",")
    major = request.args.get('major')
    semesters = int(request.args.get('semesters'))
    units = int(request.args.get('units'))
    inter = request.args.get('inter') == "true"
    math = request.args.get('math') == "true"

    school_from = ",".join(schools_from)
    return render_template('school.html',
        school_from=school_from,
        classes=handle_classes(semesters, schools_from[0], inter, units, math))
    
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
