from flask import render_template
from packages import app
@app.route('/index/')
def index():
    return render_template('index.html')

@app.route('/about/')
def about():
    return render_template('about.html')

@app.route('/search/')
def search():
    return render_template('search.html')

@app.route('/artists/')
def artists():
    return render_template('artist.html')

@app.route('/user_login/')
def user_login():
    return render_template('user_login.html')

@app.route('/user_reg/')
def user_reg():
    return render_template('user_reg.html')

@app.route('/scorers/')
def scorers():
    return render_template('scorers.html')

@app.route('/artistdash/')
def artistdash():
    return render_template('artist_dash.html')

@app.route('/admindash/')
def admindash():
    return render_template('admin_dash.html')

@app.route('/scorerdash/')
def scorerdash():
    return render_template('scorer_dash.html')

@app.route('/userdash/')
def userdash():
    return render_template('user_dash.html')

@app.route('/songs/')
def songs():
    return render_template('songs.html')

@app.route('/omemma/')
def omemma():
    return render_template('omemma.html')

@app.route('/worthy/')
def worthy():
    return render_template('worthy.html')