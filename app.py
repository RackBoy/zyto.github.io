import io
import json
import os
from flask import Flask, render_template, request, url_for
#from flask_shorturl import ShortUrl
from flask_frozen import Freezer
from flask_flatpages import FlatPages

app = Flask(__name__)
flatpage = FlatPages(app)
freezer = Freezer(app)

@freezer.register_generator
def url_generator():
    yield '/'
    yield '/projects'
    yield '/reading'
    yield '/timeline'

common = {
    'first_name': 'Joel',
    'last_name': 'Soto'
}

@app.route('/')
def index():
    return render_template('home.html', common=common)

#@freezer.register_generator

#@app.route('/projects.html') 
#@app.route('/<path:path>/') 
@app.route('/projects') 
def projects():
    data = get_static_json("static/projects/projects.json")['projects']
    data.sort(key=order_projects_by_weight, reverse=True)

    tag = request.args.get('tags')
    if tag is not None:
        data = [project for project in data if tag.lower() in [project_tag.lower() for project_tag in project['tags']]]

    return render_template('projects.html', common=common, projects=data, tag=tag)

@app.route('/reading')
def reading():
    data = get_static_json("static/files/reading.json")
    return render_template('reading.html', common=common, data=data)


@app.route('/timeline')
def timeline():
    return render_template('timeline.html', common=common)


def order_projects_by_weight(projects):
    try:
        return int(projects['weight'])
    except KeyError:
        return 0


# new here 

@app.route('/projects/<title>')
def project(title):
    projects = get_static_json("static/projects/projects.json")['projects']
    experiences = get_static_json("static/experiences/experiences.json")['experiences']

    in_project = next((p for p in projects if p['link'] == title), None)
    in_exp = next((p for p in experiences if p['link'] == title), None)

    if in_project is None and in_exp is None:
        return render_template('404.html'), 404
    # fixme: choose the experience one for now, cuz I've done some shite hardcoding here.
    elif in_project is not None and in_exp is not None:
        selected = in_exp
    elif in_project is not None:
        selected = in_project
    else:
        selected = in_exp

    # load html if the json file doesn't contain a description
    if 'description' not in selected:
        path = "experiences" if in_exp is not None else "projects"
        selected['description'] = io.open(get_static_file(
            'static/%s/%s/%s.html' % (path, selected['link'], selected['link'])), "r", encoding="utf-8").read()
    return render_template('project.html', common=common, project=selected)

#end here

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html', common=common), 404


def get_static_file(path):
    site_root = os.path.realpath(os.path.dirname(__file__))
    return os.path.join(site_root, path)


def get_static_json(path):
    return json.load(open(get_static_file(path)))

with app.test_request_context():
    #print(url_for('/'))
    print(url_for('projects'))
    print(url_for('reading'))
    print(url_for('timeline'))

if __name__ == "__main__":
    #freezer.freeze()
    #freezer.run(debug=True)
    #print("running py app")
    app.run(host="127.0.0.1", port=5000, debug=True)
