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

def handle_classes():
    gen_eds = ["English", "Japanese", "Japanese II", "Dance", "Depression"]
    gen_eds = random.sample(gen_eds, k=len(gen_eds))

    classes = ""
    for y in range(1, 4+1):
        classes += f"""
Year {y}:
{gen_eds[y%len(gen_eds)]}
"""
    return classes

@app.route('/school')
def hello():
    school_from = request.args.get('from')
    if school_from in schools:
        return render_template('school.html', school_from=school_from, classes=handle_classes())
    else:
        nearest = max(schools, key=lambda r: similar( r.upper(), school_from.upper() ))
        return render_template('school_error.html', school_from=school_from, DYM=nearest)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=25565)
