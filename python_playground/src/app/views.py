import subprocess
import os
from app import app
from flask import Flask, session, redirect, url_for, request, send_from_directory
from markupsafe import escape
from app.secrets import password, key
from app.storage import Db

app.secret_key = key


@app.route('/')
def index():
    html = '''
    <head>
        <style>
            input {
                width: 100%;
            }
            form {
                border: 1px solid black;
                max-width: 400px;
            }
            form h3 {
                margin: auto;
                text-align: center;
                border-bottom: 1px solid black;
                padding: 10px 0;
            }
            form .contents {
                padding: 10px;
            }
            table {
                border: 1px solid black;
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
    '''
    if 'username' in session:
        html += '''
            <form method="post" action="/clips">
                <h3>Generate a Clip</h3>
                <div class="contents">
                    <p><input placeholder="youtube start link" type=text name=yt-start></p>
                    <p><input placeholder="youtube stop link" type=text name=yt-stop></p>
                    <p><input placeholder="optional name" type=text name=name></p>
                    <p><input type=submit value=Generate Cip></p>
                </div>
            </form>
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
        <form method="post" action="/login">
            <p><input placeholder="password" type=password name=password>
            <p><input type=submit value=Login>
        </form>
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
