import subprocess
import os
from app import app
from flask import Flask, session, redirect, url_for, request, send_from_directory
from markupsafe import escape
from app.secrets import password, key
from app.storage import Db

app.secret_key = key

# @app.route('/', defaults={'path': ''})
# @app.route('/<path:path>')
# def catch_all(path):
#     return app.send_static_file("index.html")


@app.route('/')
def index():
    html = '''
    <head>
        <title>HeroLFG Toolbox</title>
        <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css" integrity="sha384-ggOyR0iXCbMQv3Xipma34MD+dH/1fQ784/j6cY/iJTQUOhcWr7x9JvoRxT2MZw1T" crossorigin="anonymous">
        <style>
            body {
                color: white;
            }
        </style>
        <script>
            function ready() {
                if (document.readyState !== 'complete') {
                    console.log('not ready');
                    setTimeout(ready);
                    return;
                }
                console.log('ready!');
            }
            ready();
        </script>
    </head>
    <body class="bg-dark pt-5">
    '''
    if 'username' in session:
        html += '''
            <div class="container">
                <form method="post" action="/clips">
                    <h3>Generate a Clip</h3>
                    <div class="form-group pt-2">
                        <input name="yt-start" class="form-control" id="yt-start" placeholder="YouTube Start Link">
                    </div>
                    <div class="form-group">
                        <input name="yt-stop" class="form-control" id="yt-stop" placeholder="YouTube Stop Link">
                    </div>
                    <div class="form-group">
                        <input name="name" class="form-control" id="name" placeholder="Name (optional)">
                    </div>
                    <button type="submit" class="btn btn-primary">Submit</button>
                </form>
            </div>
        '''

        db = Db()
        clip_jobs = db.get_clip_jobs
        if not clip_jobs:
            return html

        rows = ''
        for clip_job in clip_jobs():
            filename = clip_job['filename']
            name = clip_job['name']
            rows += f'''
                <tr>
                    <td><a href="/clips/{filename}">{name}</a></td>
                </tr>
            '''
        if len(rows) > 0:
            html += '<table>'
            html += '<tr><th>filename</th></tr>'
            html += rows
            html += '<table>'
        return html
    html += '''
        <div class="container">
            <form method="post" action="/login">
                <h3>Login</h3>
                <div class="form-group pt-2">
                    <input name="password" type="password" class="form-control" id="password" placeholder="Password">
                </div>
                <button type="submit" class="btn btn-primary">Submit</button>
            </form>
        </div>
        <script src="https://code.jquery.com/jquery-3.3.1.slim.min.js" integrity="sha384-q8i/X+965DzO0rT7abK41JStQIAqVgRVzpbzo5smXKp4YfRvH+8abtTE1Pi6jizo" crossorigin="anonymous"></script>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.7/umd/popper.min.js" integrity="sha384-UO2eT0CpHqdSJQ6hJty5KVphtPhzWj9WO1clHTMGa3JDZwrnQq4sF86dIHNDz0W1" crossorigin="anonymous"></script>
        <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/js/bootstrap.min.js" integrity="sha384-JjSmVgyd0p3pXB1rRibZUAYoIIy6OrQ6VrjIEaFf/nJGzIxFDsf4x0xIM+B07jRM" crossorigin="anonymous"></script>
    </body>
    '''
    return html


@app.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        if request.form['password'] == password:
            session['username'] = 'user'
            return redirect(url_for('index'))
        return redirect(url_for('index'))

@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('username', None)
    return redirect(url_for('index'))

@app.route('/clips', methods=['POST'])
def clip():
    if request.method == 'POST':
        start_link = request.form['yt-start']
        stop_link = request.form['yt-stop']
        name = request.form['name']
        print(f'start:{start_link}')
        print(f'stop:{stop_link}')
        print(f'name:{name}')
        db = Db()
        db.save_new_clip_job(start_link, stop_link, name)
        cmd = f'python /application/scripts/youtube/clip.py {start_link} {stop_link}'
        print(cmd)
        subprocess.Popen(['python', '/application/scripts/youtube/clip.py', start_link, stop_link])
        return redirect(url_for('index'))

@app.route('/clips/<path:filename>')
def download_file(filename):
    return send_from_directory('/application/clips', filename, as_attachment=True)
