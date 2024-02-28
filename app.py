import json, os.path
from flask import Flask, render_template, request, redirect, url_for, flash, abort, session, jsonify, Blueprint
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = 'fsagtehbsf4rsdf'

# bp = Blueprint('urlshort', __name__)


@app.route('/')
def home():
    return render_template('home.html', codes=session.keys())


@app.route('/your-url', methods=['GET', 'POST'])
def your_url():
    if request.method == 'POST':
        urls = {}

        if os.path.exists('urls.json'):
            with open('urls.json') as urls_file:
                urls = json.load(urls_file)  # load the existing file

        if request.form['code'] in urls.keys():
            flash('Short name not available. Select another')
            return redirect(url_for('home'))

        if 'url' in request.form.keys():
            urls[request.form['code']] = {'url': request.form['url']}  # Dictionary with data
        else:
            f = request.files['file']  # Retrieving the file from the html
            full_name = request.form['code'] + secure_filename(f.filename)
            f.save('D:/IIT Docs/2nd Year/Semester 1/CM 2603 - Data Science '
                   'Project/Project/SampleFlask/flaskProject/static/user_files/'
                   + full_name)
            urls[request.form['code']] = {'file': full_name}

        with open('urls.json', 'w') as url_file:
            json.dump(urls, url_file)
            session[request.form['code']] = True
        return render_template('your_url.html', code=request.form['code'])
        # the shorten name for the url is retrieved
    else:
        return redirect(url_for('home'))  # Redirect to home page, same url as home page


@app.route('/<string:code>')
def redirect_url(code):
    if os.path.exists('urls.json'):
        with open('urls.json') as urls_file:
            urls = json.load(urls_file)
            if code in urls.keys():
                if 'url' in urls[code].keys():
                    return redirect(urls[code]['url'])
                else:
                    return redirect(url_for('static', filename='user_files/' + urls[code]['file']))

    return abort(404)


@app.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'), 404


@app.route('/api')
def session_api():
    return jsonify(list(session.keys()))
